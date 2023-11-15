import json
import pyrebase


class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
       
    def insert_item(self, name, data):
        item_info ={
            "sellerId": data['seller-id'],
            "productName": data['product-name'],
            "productPrice": data['product-price'],
            # "currentLocation": data['currentLocation'],
            "product-status": data['product-status'],
            "description": data['product-description'],
            # "product-image": img_path
        }
        self.db.child("item").child(name).set(item_info)
        print(data)
        return True
        