import pickle

import joblib
import pandas as pd


class ProductEncoder:
    def __init__(
        self,
        product_rankings: pd.DataFrame(),
        product_dim: pd.DataFrame(),
        num_products: int,
    ):
        self.product_rankings = product_rankings

        # Convert product ID to INDEX (ordered by most popular to least popular items)
        self.product_to_idx = {
            p: (i if i < num_products else 0) for p, i in self.product_rankings.values
        }

        # Convert INDEX back to product number
        self.idx_to_product = {i: p for p, i in self.product_to_idx.items() if i > 0}

        # Departments
        self.dept_decode = {
            1: "frozen",
            2: "other",
            3: "bakery",
            4: "produce",
            5: "alcohol",
            6: "international",
            7: "beverages",
            8: "pets",
            9: "dry goods pasta",
            10: "bulk",
            11: "personal care",
            12: "meat seafood",
            13: "pantry",
            14: "breakfast",
            15: "canned goods",
            16: "dairy eggs",
            17: "household",
            18: "babies",
            19: "snacks",
            20: "deli",
            21: "missing",
        }

        # Product information
        self.product_dict = {
            prod_id: {
                "product_id": prod_id,
                "product_name": prod_name,
                "aisle_id": aisle,
                "department_id": dept,
                "department_name": self.dept_decode[dept],
            }
            for prod_id, prod_name, aisle, dept in product_dim.values
        }

    def decode_product_idx(self, idx: int):
        """Get product information from encoded index position"""
        if idx in self.idx_to_product:
            return self.product_dict[self.idx_to_product[idx]]
        else:
            return {
                "product_name": "Unknown",
                "aisle_id": -1,
                "department_id": -1,
                "department_name": "missing",
            }
