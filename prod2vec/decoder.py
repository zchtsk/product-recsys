import json
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
            p: rnk if rnk < num_products else 0 for p, rnk in self.product_rankings.values
        }

        # Convert INDEX back to product number
        self.idx_to_product = {i: p for p, i in self.product_to_idx.items() if i > 0}

        # Department and Aisle Information
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

        self.aisle_decode = {
            1: "prepared soups salads",
            2: "specialty cheeses",
            3: "energy granola bars",
            4: "instant foods",
            5: "marinades meat preparation",
            6: "other",
            7: "packaged meat",
            8: "bakery desserts",
            9: "pasta sauce",
            10: "kitchen supplies",
            11: "cold flu allergy",
            12: "fresh pasta",
            13: "prepared meals",
            14: "tofu meat alternatives",
            15: "packaged seafood",
            16: "fresh herbs",
            17: "baking ingredients",
            18: "bulk dried fruits vegetables",
            19: "oils vinegars",
            20: "oral hygiene",
            21: "packaged cheese",
            22: "hair care",
            23: "popcorn jerky",
            24: "fresh fruits",
            25: "soap",
            26: "coffee",
            27: "beers coolers",
            28: "red wines",
            29: "honeys syrups nectars",
            30: "latino foods",
            31: "refrigerated",
            32: "packaged produce",
            33: "kosher foods",
            34: "frozen meat seafood",
            35: "poultry counter",
            36: "butter",
            37: "ice cream ice",
            38: "frozen meals",
            39: "seafood counter",
            40: "dog food care",
            41: "cat food care",
            42: "frozen vegan vegetarian",
            43: "buns rolls",
            44: "eye ear care",
            45: "candy chocolate",
            46: "mint gum",
            47: "vitamins supplements",
            48: "breakfast bars pastries",
            49: "packaged poultry",
            50: "fruit vegetable snacks",
            51: "preserved dips spreads",
            52: "frozen breakfast",
            53: "cream",
            54: "paper goods",
            55: "shave needs",
            56: "diapers wipes",
            57: "granola",
            58: "frozen breads doughs",
            59: "canned meals beans",
            60: "trash bags liners",
            61: "cookies cakes",
            62: "white wines",
            63: "grains rice dried goods",
            64: "energy sports drinks",
            65: "protein meal replacements",
            66: "asian foods",
            67: "fresh dips tapenades",
            68: "bulk grains rice dried goods",
            69: "soup broth bouillon",
            70: "digestion",
            71: "refrigerated pudding desserts",
            72: "condiments",
            73: "facial care",
            74: "dish detergents",
            75: "laundry",
            76: "indian foods",
            77: "soft drinks",
            78: "crackers",
            79: "frozen pizza",
            80: "deodorants",
            81: "canned jarred vegetables",
            82: "baby accessories",
            83: "fresh vegetables",
            84: "milk",
            85: "food storage",
            86: "eggs",
            87: "more household",
            88: "spreads",
            89: "salad dressing toppings",
            90: "cocoa drink mixes",
            91: "soy lactosefree",
            92: "baby food formula",
            93: "breakfast bakery",
            94: "tea",
            95: "canned meat seafood",
            96: "lunch meat",
            97: "baking supplies decor",
            98: "juice nectars",
            99: "canned fruit applesauce",
            100: "missing",
            101: "air fresheners candles",
            102: "baby bath body care",
            103: "ice cream toppings",
            104: "spices seasonings",
            105: "doughs gelatins bake mixes",
            106: "hot dogs bacon sausage",
            107: "chips pretzels",
            108: "other creams cheeses",
            109: "skin care",
            110: "pickled goods olives",
            111: "plates bowls cups flatware",
            112: "bread",
            113: "frozen juice",
            114: "cleaning products",
            115: "water seltzer sparkling water",
            116: "frozen produce",
            117: "nuts seeds dried fruit",
            118: "first aid",
            119: "frozen dessert",
            120: "yogurt",
            121: "cereal",
            122: "meat counter",
            123: "packaged vegetables fruits",
            124: "spirits",
            125: "trail mix snack mix",
            126: "feminine care",
            127: "body lotions soap",
            128: "tortillas flat bread",
            129: "frozen appetizers sides",
            130: "hot cereal pancake mixes",
            131: "dry pasta",
            132: "beauty",
            133: "muscles joints pain relief",
            134: "specialty wines champagnes",
        }

        # Product information
        self.product_dict = {
            prod_id: {
                "product_id": prod_id,
                "product_name": prod_name,
                "aisle_id": aisle,
                "aisle_name": self.aisle_decode[aisle],
                "department_id": dept,
                "department_name": self.dept_decode[dept],
            }
            for prod_id, prod_name, aisle, dept in product_dim.values
        }

    def decode_product_idx(self, idx: int):
        """Get product information from encoded index position"""
        if idx in self.idx_to_product and self.idx_to_product[idx] in self.product_dict:
            data = self.product_dict[self.idx_to_product[idx]]
            return json.loads(json.dumps(data))
        else:
            return {
                "product_id": -1,
                "product_name": "unknown",
                "aisle_id": -1,
                "aisle_name": "missing",
                "department_id": -1,
                "department_name": "missing",
            }
