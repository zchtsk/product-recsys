#!/bin/bash

# Download Instacart dataset using Kaggle CLI
# Requires Kaggle API credentials to be set up

set -e

DATASET="psparks/instacart-market-basket-analysis"
OUTPUT_DIR="datalake"

echo "Downloading Instacart dataset..."

# Check if kaggle CLI is installed
if ! command -v kaggle &> /dev/null; then
    echo "Kaggle CLI not found. Installing..."
    pip install kaggle
fi

# Check if data already exists
if [ -f "$OUTPUT_DIR/order_products__train.csv" ] && [ -f "$OUTPUT_DIR/products.csv" ]; then
    echo "Dataset files already exist, skipping download."
    exit 0
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Download and extract dataset
echo "Downloading $DATASET to $OUTPUT_DIR..."
kaggle datasets download -d "$DATASET" -p "$OUTPUT_DIR" --unzip

echo "Dataset downloaded successfully!"

# List downloaded files
echo "Downloaded files:"
ls -la "$OUTPUT_DIR"/*.csv