import joblib
import numpy as np
import pandas as pd

from gensim.models import Word2Vec

from decoder import ProductEncoder

### GLOBALS
NUM_PRODUCTS = 2000


def main():
    ### Datasets
    products = pd.read_csv("../datalake/products.csv")
    orders = pd.read_csv("../datalake/order_products__train.csv")

    ### Take in order x product combinations
    ### Return products ranked by number of orders they appear in
    product_ranking = (
        orders.groupby("product_id")
        .agg(ct=("order_id", "count"))
        .reset_index()
        .sort_values(["ct"], ascending=False)
        .assign(rank=lambda d: d.reset_index().index + 1)
        .drop(["ct"], axis=1)
    )

    # Save produce encoder/decoder
    prod_encoder = ProductEncoder(product_ranking, products, num_products=NUM_PRODUCTS)
    with open("../datalake/product_encoder.pkl", "wb") as f:
        joblib.dump(prod_encoder, f)

    ### Aggregate orders
    baskets = (
        orders.groupby("order_id")["product_id"]
        .apply(list)
        .reset_index()["product_id"]
        .apply(lambda ls: [prod_encoder.product_to_idx[x] for x in ls])
    )

    ### Prod2Vec model
    model = Word2Vec(sentences=baskets, vector_size=64, negative=20, seed=42)
    model.save("../datalake/prod2vec.model")

    # Save basket encodings
    with open("../datalake/basket_encodings.npy", "wb") as f:
        np.save(f, np.array(baskets.values), allow_pickle=True)

    # Save basket embeddings
    basket_embeddings = [list(np.sum(model.wv[p], axis=0)) for p in baskets]
    with open("../datalake/basket_embeddings.npy", "wb") as f:
        np.save(f, basket_embeddings, allow_pickle=True)


if __name__ == "__main__":
    main()
