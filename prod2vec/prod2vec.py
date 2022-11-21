import numpy as np

from utils import (
    get_minio_client,
    download_dataframe,
    save_numpy,
    save_w2v_model,
    save_joblib_obj,
)

from gensim.models import Word2Vec

from decoder import ProductEncoder

### GLOBALS
NUM_PRODUCTS = 2000


def main():
    ### Datasets
    minio_client = get_minio_client()
    products = download_dataframe(minio_client, "products.csv")
    orders = download_dataframe(minio_client, "order_products__train.csv")

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
    save_joblib_obj(minio_client, prod_encoder, "product_encoder.pkl")

    ### Aggregate orders
    baskets = (
        orders.groupby("order_id")["product_id"]
        .apply(list)
        .reset_index()["product_id"]
        .apply(lambda ls: [prod_encoder.product_to_idx[x] for x in ls])
    )

    ### Prod2Vec model
    model = Word2Vec(sentences=baskets, vector_size=64, negative=20, seed=42)
    save_w2v_model(minio_client, model, "prod2vec.model")

    # Save basket encodings
    save_numpy(minio_client, baskets.values, "basket_encodings.npy")

    # Save basket embeddings
    basket_embeddings = [list(np.sum(model.wv[p], axis=0)) for p in baskets]
    save_numpy(minio_client, basket_embeddings, "basket_embeddings.npy")


if __name__ == "__main__":
    main()
