import os

from minio import Minio
from pytest import fixture


@fixture(scope="module")
def minio_client():
    client = Minio(
        endpoint=os.environ["MINIO_ENDPOINT"],
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=False if os.environ["RUNTIME"] == "dev" else True,
    )
    return client