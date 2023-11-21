from flask import Flask, render_template, request
from database import DBhandler

import sys


application = Flask(__name__)


DB = DBhandler()


@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/list")
def view_list():
    return render_template("list.html")


@application.route("/review") 
def view_review():
    return render_template("review.html")


@application.route("/reg_items", methods=['GET', 'POST']) 
def reg_item():
    return render_template("reg_items.html")


@application.route("/reg_reviews") 
def reg_review():
    return render_template("reg_reviews.html")


@application.route("/submit_items_post", methods=['POST']) 
def reg_item_submit_post():
    file = request.files['productImage']
    data = {
        "seller-id" : request.form.get("sellerId"),
        "product-name" : request.form.get("productName"),
        "product-price" : request.form.get("productPrice"),
        "product-status" : request.form.get("condition"),
        "product-description" : request.form.get("productDescription")
    } 
    if 'productImage' in request.files:
        file = request.files['productImage']
        # 파일을 어디에 저장할지 결정하고 저장합니다.
        img_path = "./static/images/" + file.filename
        file.save(img_path)
        data['img_path'] = img_path
    
    DB.insert_item(data['product-name'], data)
    return render_template("submit_item_result.html", data=data)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
    