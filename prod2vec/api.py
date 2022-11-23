import json
import os
from collections import Counter, defaultdict
from typing import List

import joblib
import numpy as np
from flask import Flask
from flask_cors import CORS
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity

import pathlib

### Preload Model & Embedding information
root_path = pathlib.Path(__file__).parent
prod_encoder = joblib.load(str(root_path / "../datalake/product_encoder.pkl"))
prod2vec = Word2Vec.load(str(root_path / "../datalake/prod2vec.model"))
basket_encodings = np.load(
    str(root_path / "../datalake/basket_encodings.npy"), allow_pickle=True
)
basket_embeddings = np.load(
    str(root_path / "../datalake/basket_embeddings.npy"), allow_pickle=True
)

app = Flask(__name__)
cors = CORS(
    app,
    resources={r"/*": {"origins": [os.environ["CLIENT_ENDPOINT"]]}},
    support_credentials=True
)


@app.route("/")
def hello_world():
    return "world"


@app.route("/similar/<int:item_idx>")
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


def get_complement_items(
    orig_basket: List[int], candidate_baskets: List[List[int]], nitems: int = 5
):
    items = Counter()
    for bsk in candidate_baskets:
        for itm in bsk:
            if itm > 0 and itm not in orig_basket:
                items[itm] += 1
    return [prod_encoder.decode_product_idx(x[0]) for x in items.most_common(nitems)]


@app.route("/basket/")
@app.route("/basket/<int:basket_idx>")
def get_basket_info(basket_idx: int = 0):
    while basket_idx == 0 or sum(basket_encodings[basket_idx]) == 0:
        basket_idx = np.random.randint(1, 8_500)
        items = basket_encodings[basket_idx]
    else:
        items = basket_encodings[basket_idx]
    item_descs = []

    # Get item descriptions and find item substitutes
    for x in items:
        if x > 0:
            data_dict = prod_encoder.decode_product_idx(x)
            data_dict["id"] = int(x)
            try:
                data_dict["subs"] = get_similar_items(x, 0.85)
            except:
                data_dict["subs"] = []
            data_dict["show_subs"] = False
            item_descs.append(data_dict)

    # Organize Basket by departments
    departments = defaultdict(list)
    for itm in item_descs:
        departments[itm["department_name"]].append(itm)

    # Find complement items
    bsk_embedding = get_basket_embedding(basket_idx)
    candidates = get_complement_baskets(bsk_embedding, threshold=0.97)
    complements = get_complement_items(list(items), candidates, 4)

    # Organize Complements by departments
    compl_depts = defaultdict(list)
    for itm in complements:
        compl_depts[itm["department_name"]].append(itm)

    return dict(
        data=departments,
        also_like=compl_depts,
        show_also_like=False,
        basket_id=basket_idx,
    )
