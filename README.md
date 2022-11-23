# Grocery Product Recommendations
This project looks at grocery retail transaction data and applies a Word2Vec model to generate embeddings for individual products. 
Similarity between items can then be determined with cosine similarity scores to generate lists of substitutes. 
We can also use these embeddings to compare entire baskets to each other, and then look for items that similar shoppers purchased.

Live demo can be accessed [**here**](https://recsys-client-7zy464zyhq-uc.a.run.app/)

https://user-images.githubusercontent.com/109352381/203448258-11fb6807-33cc-4482-81b7-220765c9ee0a.mp4


# Process
(1) Product Mapping Dictionary
* Import transaction information.
* Rank unique items based on how many orders they appear in.
* Create a mapping function to translate a given product_id to it's rank order.
* This new ranking id is what we'll use for any reference to given product.

(2) Product Embedding
* Import transaction information.
* Group by order_id and collect a list of unique items in that order.
* Use our Product Mapping Dictionary to translate product_ids to rank order ids.
* At this point you should have a list of customer baskets, and each basket should have your converted product IDs.
* This will be the input for training our Word2Vec model and generating embeddings.

(3) Substitute Items
* After generating product embedding, perform a simple cosine similarity comparison to identify the top N similar items.

(4) Recommended Items
* For a given basket, sum up the product embeddings. This will represent our basket's embedding.
* Perform the same action for all other baskets, then perform cosine similar comparison to find the N most similar baskets.
* Look for the top items in these baskets that do not appear in the basket being examined.

# Examples
### Use product embedding to find similar items...
![ApplicationFrameHost_1PVGMRJMsA](https://user-images.githubusercontent.com/109352381/203446366-022e2471-b32e-43f0-9b50-fac5643feb0b.png)

### Find products purchased in similar baskets...
![ApplicationFrameHost_Tor7XqarRj](https://user-images.githubusercontent.com/109352381/203446383-f65773ca-b1a1-4dcc-a21f-a4fe4cfb0f51.png)

# Development Notes
* Using "Kaggle Market Basket Analysis" dataset, which can be found [here](https://www.kaggle.com/competitions/instacart-market-basket-analysis/data)
* Unzip and make sure the `products.csv` and `orders.csv` files are in the `datalake` folder
