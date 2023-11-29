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


    
    def insert_user(self, data, pw):
        user_info = {
            "id": data['id'],
            "password": pw,
            "nickname": data['nickname']
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

        return result

    
    def get_all_reviews(self ):
        reviews = self.db.child("review").get().val()
        return reviews
    
    def find_user(self, id_, pw_):
        users = self.db.child("user").get() 
        target_value=[]
        for res in users.each():
            value = res.val()
            
            if value['id'] == id_ and value['password'] == pw_:
                return True 
            
        return False

    def reg_review(self, data):
        review_info = {
            "title": data['title'],
            "point": data['point'],
            "content": data['content'],
            "img_path": data['img_path'],
            "authorId": data['authorId']
        }
        self.db.child("review").child(data['productName']).set(review_info)
        return True
    
    def get_item_byname(self, name): 
        items = self.db.child("item").get() 
        target_value="" 
        print("###########",name)
        for res in items.each(): 
            key_value = res.key()
            if key_value == name: 
                target_value=res.val()
        return target_value
            
    def get_review_byname(self, name): 
        reviews = self.db.child("review").get() 
        target_value="" 
        print("###########",name)
        for res in reviews.each():
            key_value = res.key()
            if key_value == name: 
                target_value=res.val()
                break

        return target_value
        
    def get_heart_byname(self, uid, name):
        hearts = self.db.child("heart").child(uid).get()
        target_value=""
        if hearts.val() == None:
            return target_value

        for res in hearts.each():
            key_value = res.key()

        if key_value == name:
            target_value=res.val()
            return target_value
    
    def update_heart(self, user_id, isHeart, item):
        heart_info ={
             "interested": isHeart
        }
        self.db.child("heart").child(user_id).child(item).set(heart_info)
        return True
