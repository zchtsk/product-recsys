#!/bin/bash

set -e

echo "=== Product RecSys Initialization ==="

# Check if model files already exist
if [ -f "/datalake/prod2vec.model" ] && [ -f "/datalake/product_encoder.pkl" ]; then
    echo "✅ Model files already exist, starting API server..."
    exec uv run gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 api:app
fi

echo "🔄 Model files not found, initializing data and training..."

# Check if data files exist
if [ ! -f "/datalake/order_products__train.csv" ] || [ ! -f "/datalake/products.csv" ]; then
    echo "📥 Downloading Instacart dataset..."
    uv run python /app/scripts/download_data.py
    
    # Copy downloaded files to datalake if they were downloaded to a different location
    if [ -f "/app/order_products__train.csv" ]; then
        cp /app/order_products__train.csv /datalake/
    fi
    if [ -f "/app/products.csv" ]; then
        cp /app/products.csv /datalake/
    fi
else
    echo "✅ Data files already exist"
fi

# Train the model
echo "🤖 Training Word2Vec model..."
cd /app
uv run python prod2vec.py

echo "✅ Training complete! Starting API server..."
exec uv run gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 api:app