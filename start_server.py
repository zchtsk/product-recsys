#!/usr/bin/env python3
"""
Initialization and startup script for Product RecSys API
"""
import os
import sys
import pathlib
import subprocess

def check_model_files_exist():
    """Check if model files already exist"""
    model_path = pathlib.Path("/datalake/prod2vec.model")
    encoder_path = pathlib.Path("/datalake/product_encoder.pkl")
    return model_path.exists() and encoder_path.exists()

def check_data_files_exist():
    """Check if data files already exist"""
    data_path = pathlib.Path("/datalake")
    return (data_path / "order_products__train.csv").exists() and (data_path / "products.csv").exists()

def download_data():
    """Download the dataset"""
    print("📥 Downloading Instacart dataset...")
    try:
        result = subprocess.run([
            "python", "/app/scripts/download_data.py"
        ], check=True, cwd="/app", capture_output=True, text=True)
        print("✅ Dataset downloaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading dataset: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def train_model():
    """Train the Word2Vec model"""
    print("🤖 Training Word2Vec model...")
    try:
        result = subprocess.run([
            "python", "prod2vec.py"
        ], check=True, cwd="/app", capture_output=True, text=True)
        print("✅ Model training completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error training model: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def start_api_server():
    """Start the API server"""
    print("🚀 Starting API server...")
    port = os.environ.get("PORT", "5000")
    
    try:
        subprocess.run([
            "gunicorn", 
            "--bind", f":{port}",
            "--workers", "1",
            "--threads", "8", 
            "--timeout", "0",
            "api:app"
        ], check=True, cwd="/app")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

def main():
    print("=== Product RecSys Initialization ===")
    
    # Check if model files already exist
    if check_model_files_exist():
        print("✅ Model files already exist, starting API server...")
        start_api_server()
        return
    
    print("🔄 Model files not found, initializing data and training...")
    
    # Check if data files exist, if not download them
    if not check_data_files_exist():
        if not download_data():
            print("❌ Failed to download dataset, exiting...")
            sys.exit(1)
    else:
        print("✅ Data files already exist")
    
    # Train the model
    if not train_model():
        print("❌ Failed to train model, exiting...")
        sys.exit(1)
    
    print("✅ Initialization complete! Starting API server...")
    start_api_server()

if __name__ == "__main__":
    main()