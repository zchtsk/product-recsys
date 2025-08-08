#!/usr/bin/env python3
"""
Download Instacart dataset from Kaggle
"""
import os
import sys
import zipfile
import requests
from pathlib import Path


def download_kaggle_dataset(dataset_url: str, output_dir: str):
    """Download and extract Kaggle dataset"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Check if files already exist
    required_files = [
        output_path / "order_products__train.csv",
        output_path / "products.csv"
    ]
    
    if all(f.exists() for f in required_files):
        print("Dataset files already exist, skipping download.")
        return
    
    print(f"Downloading dataset from {dataset_url}")
    
    try:
        # Download the zip file
        response = requests.get(dataset_url, stream=True)
        response.raise_for_status()
        
        zip_path = output_path / "instacart-dataset.zip"
        
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded to {zip_path}")
        
        # Extract the zip file
        print("Extracting dataset...")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_path)
        
        # Clean up the zip file
        zip_path.unlink()
        
        print("Dataset downloaded and extracted successfully!")
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading dataset: {e}")
        print("You may need to:")
        print("1. Set up Kaggle API credentials")
        print("2. Use: kaggle datasets download -d psparks/instacart-market-basket-analysis -p datalake/")
        sys.exit(1)


def main():
    dataset_url = "https://www.kaggle.com/api/v1/datasets/download/psparks/instacart-market-basket-analysis"
    output_dir = "/datalake"
    
    download_kaggle_dataset(dataset_url, output_dir)


if __name__ == "__main__":
    main()