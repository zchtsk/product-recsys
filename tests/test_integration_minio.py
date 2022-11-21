from prod2vec.utils import BytesIO, download_dataframe, save_numpy, download_numpy

import numpy as np
import pandas as pd


def test_download_dataframe(minio_client):
    dummy_data = [
        {
            "product_id": 1,
            "product_name": "Chocolate Sandwich Cookies",
            "aisle_id": 61,
            "department_id": 19,
        },
        {
            "product_id": 2,
            "product_name": "All-Seasons Salt",
            "aisle_id": 104,
            "department_id": 13,
        },
        {
            "product_id": 3,
            "product_name": "Robust Golden Unsweetened Oolong Tea",
            "aisle_id": 94,
            "department_id": 7,
        },
    ]
    downloaded_data = download_dataframe(minio_client, "products.csv")[:3].to_dict(
        "records"
    )
    assert dummy_data == downloaded_data


def test_put_pd_obj_to_minio(minio_client):
    dummy_data = [
        {
            "product_id": 1,
            "product_name": "Chocolate Sandwich Cookies",
            "aisle_id": 61,
            "department_id": 19,
        },
        {
            "product_id": 2,
            "product_name": "All-Seasons Salt",
            "aisle_id": 104,
            "department_id": 13,
        },
        {
            "product_id": 3,
            "product_name": "Robust Golden Unsweetened Oolong Tea",
            "aisle_id": 94,
            "department_id": 7,
        },
    ]

    csv_bytes = pd.DataFrame(dummy_data).to_csv(index=False).encode("utf-8")
    csv_buffer = BytesIO(csv_bytes)
    minio_client.put_object(
        "bucket",
        "tmp_data.csv",
        csv_buffer,
        length=len(csv_bytes),
        content_type="application/csv",
    )
    downloaded_data = download_dataframe(minio_client, "tmp_data.csv").to_dict(
        "records"
    )
    assert dummy_data == downloaded_data


def test_minio_save_and_load_numpy(minio_client):
    data = np.array([[1, 2, 3], [1, 2, 3]])

    # Write to temp
    save_numpy(minio_client, data, "tmp.npy")

    # Read file
    arr = download_numpy(minio_client, "tmp.npy")
    assert all(np.array(arr == data).flatten())
