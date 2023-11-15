import json
import pyrebase


class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config = json.load(f)

        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
       
    def insert_item(self, name, data, img_path):
        item_info ={
            "sellerId": data['sellerId'],
            "productName": data['productName'],
            "productPrice": data['productPrice'],
            "currentLocation": data['currentLocation'],
            "card": data['card'],
            "productDescription": data['productDescription'],
            "productImage": img_path
        }
        self.db.child("item").child(name).set(item_info)
        print(data, img_path)
        return True
        