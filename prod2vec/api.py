from collections import Counter, defaultdict
from typing import List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from prod2vec import main
from utils import get_minio_client, load_joblib_obj, load_w2v_model, download_numpy

### Preload Models
try:
    minio_client = get_minio_client()
    prod_encoder = load_joblib_obj(minio_client, "product_encoder.pkl")
    prod2vec = load_w2v_model(minio_client, "prod2vec.model")
    basket_encodings = download_numpy(minio_client, "basket_encodings.npy")
    basket_embeddings = download_numpy(minio_client, "basket_embeddings.npy")
except:
    main()
    minio_client = get_minio_client()
    prod_encoder = load_joblib_obj(minio_client, "product_encoder.pkl")
    prod2vec = load_w2v_model(minio_client, "prod2vec.model")
    basket_encodings = download_numpy(minio_client, "basket_encodings.npy")
    basket_embeddings = download_numpy(minio_client, "basket_embeddings.npy")

app = FastAPI()

origins = [
    # Local Sveltekit location
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/similar/{item_idx}")
def get_similar_items(item_idx: int, threshold: float = 0):
    orig_item = prod_encoder.decode_product_idx(item_idx)
    similar = prod2vec.wv.most_similar(item_idx, topn=5)
    # Apply threshold and remove any items with IDX=0 (unknown items)
    similar = [x for x in similar if threshold <= x[1] < 1 and x[0] != 0]
    product_info = []
    # Only include items that are similar and appear in the same aisle
    for x in similar:
        xdata = prod_encoder.decode_product_idx(x[0])
        if xdata["aisle_id"] == orig_item["aisle_id"]:
            product_info.append(xdata)
    return product_info


### Basket Predictions
def get_basket_embedding(bsk_id):
    return basket_embeddings[bsk_id]


def get_complement_baskets(basket_embedding, threshold=0.95):
    idx_similar = np.array(
        cosine_similarity([basket_embedding], basket_embeddings) > threshold
    ).reshape(-1)
    similar_baskets = basket_encodings[idx_similar]
    return similar_baskets


def get_complement_items(orig_basket: List[int], candidate_baskets: List[List[int]]):
    items = Counter()
    for bsk in candidate_baskets:
        for itm in bsk:
            if itm > 0 and itm not in orig_basket:
                items[itm] += 1
    return [prod_encoder.decode_product_idx(x[0]) for x in items.most_common(5)]


@app.get("/basket/{basket_idx}")
def get_basket_info(basket_idx: int = 0):
    items = basket_encodings[basket_idx]
    item_descs = []

    # Get item descriptions and find item substitutes
    for x in items:
        if x > 0:
            data_dict = prod_encoder.decode_product_idx(x)
            data_dict["id"] = int(x)
            data_dict["subs"] = get_similar_items(x, 0.85)
            item_descs.append(data_dict)

    # Organize Basket by departments
    departments = defaultdict(list)
    for itm in item_descs:
        departments[itm["department_name"]].append(itm)

    # Find complement items
    bsk_embedding = get_basket_embedding(basket_idx)
    candidates = get_complement_baskets(bsk_embedding)
    complements = get_complement_items(items, candidates)

    return dict(data=departments, also_like=complements)
