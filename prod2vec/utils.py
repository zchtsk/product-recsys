import os
import pathlib
import pickle
import tempfile
from io import BytesIO
from typing import Any

import joblib
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from minio import Minio

def get_minio_client():
    return Minio(
        endpoint=os.environ["MINIO_ENDPOINT"],
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=False if os.environ["RUNTIME"] == "dev" else True,
    )


def save_joblib_obj(minio_client: Minio, obj: Any, filename: str) -> None:
    """Save joblib object to Minio bucket"""
    with tempfile.TemporaryDirectory() as tempdir:
        tmp_filepath = str(pathlib.Path(tempdir) / "temp_obj.pkl")
        with open(tmp_filepath, "wb") as f:
            joblib.dump(obj, f)
        minio_client.fput_object("bucket", filename, tmp_filepath)


def load_joblib_obj(minio_client: Minio, filename: str):
    """Load joblib object to Minio bucket"""
    with tempfile.TemporaryDirectory() as tempdir:
        filepath = str(pathlib.Path(tempdir) / filename)
        minio_client.fget_object("bucket", filename, filepath)
        with open(filepath, "rb") as f:
            return joblib.load(f)


def save_w2v_model(minio_client: Minio, model: Word2Vec, filename: str):
    """Save Word2Vec object to Minio bucket"""
    with tempfile.TemporaryDirectory() as tempdir:
        tmp_filepath = str(pathlib.Path(tempdir) / "temp_mdl.model")
        with open(tmp_filepath, "wb") as f:
            model.save(f, separately=[], sep_limit=1_000_000_000)
        minio_client.fput_object("bucket", filename, tmp_filepath)


def load_w2v_model(minio_client: Minio, filename) -> Word2Vec:
    """Load Word2Vec object to Minio bucket"""
    with tempfile.TemporaryDirectory() as tempdir:
        filepath = str(pathlib.Path(tempdir) / filename)
        minio_client.fget_object("bucket", filename, filepath)
        return Word2Vec.load(filepath)


def save_dataframe(minio_client: Minio, df: pd.DataFrame, filename: str) -> None:
    """Save pandas DataFrame to Minio bucket"""
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    csv_buffer = BytesIO(csv_bytes)
    minio_client.put_object(
        "bucket",
        filename,
        csv_buffer,
        length=len(csv_bytes),
        content_type="application/csv",
    )


def download_dataframe(minio_client: Minio, filename: str) -> pd.DataFrame:
    """Download file from Minio bucket"""
    with tempfile.TemporaryDirectory() as tempdir:
        filepath = pathlib.Path(tempdir) / filename
        minio_client.fget_object("bucket", filename, str(filepath))
        df = pd.read_csv(filepath)
        return df


def save_numpy(minio_client: Minio, arr: np.ndarray, filename: str) -> None:
    """Save numpy array object to Minio bucket"""
    with tempfile.TemporaryDirectory() as tempdir:
        tmp_filepath = str(pathlib.Path(tempdir) / "temp_arr.npy")
        with open(tmp_filepath, "wb") as f:
            np.save(f, arr, allow_pickle=True)
        minio_client.fput_object("bucket", filename, tmp_filepath)


def download_numpy(minio_client: Minio, filename: str) -> np.ndarray:
    """Download file from Minio bucket"""
    with tempfile.TemporaryDirectory() as tempdir:
        filepath = str(pathlib.Path(tempdir) / filename)
        minio_client.fget_object("bucket", filename, filepath)
        with open(filepath, "rb") as f:
            return np.load(f, allow_pickle=True)
