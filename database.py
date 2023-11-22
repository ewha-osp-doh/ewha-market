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
            "product-status": data['product-status'],
            "description": data['product-description'],
            "product-image": data['img_path']
        }
        self.db.child("item").child(name).set(item_info)
        print(data)
        return True


    
    def insert_user(self, data):
        user_info = {
            "id": data['id'],
            "password": data['password'],
            "email": data['email'],
            "phone": data['phone']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False

    
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()

        print("users###", users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()

                if value['id'] == id_string:
                    return False
            return True
    
    def get_all_items(self):
        items = self.db.child("item").get()
        result = []

        if items.val():
            for item in items.each():
                result.append(item.val())


    
    def find_user(self, id_, pw_):
        users = self.db.child("user").get() 
        target_value=[]
        for res in users.each():
            value = res.val()
            
            if value['id'] == id_ and value['password'] == pw_:
                return True 
            
        return False