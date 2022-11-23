# Grocery Product Recommendations
This project looks at grocery retail transaction data and applies a Word2Vec model to generate embeddings for individual products. 
Similarity between items can then be determined with cosine similarity scores, to generate lists of substitutes. 
We can also perform simple recommendations by summing up the product embeddings within a given basket and comparing this to other baskets, then looking for items similar shoppers purchased.

# Process


# Examples
### Using these product embeddings we can identify product substitutes...
![ApplicationFrameHost_1PVGMRJMsA](https://user-images.githubusercontent.com/109352381/203446366-022e2471-b32e-43f0-9b50-fac5643feb0b.png)

### We can also look for similar baskets and recommend other items people purchased...
![ApplicationFrameHost_Tor7XqarRj](https://user-images.githubusercontent.com/109352381/203446383-f65773ca-b1a1-4dcc-a21f-a4fe4cfb0f51.png)

# Development Notes
* Using "Kaggle Market Basket Analysis" dataset, which can be found [here](https://www.kaggle.com/competitions/instacart-market-basket-analysis/data)
* Unzip and make sure the `products.csv` and `orders.csv` files are in the `datalake` folder
