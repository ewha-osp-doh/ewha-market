from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler
import hashlib
import sys


application = Flask(__name__)
application.config["SECRET_KEY"] = "hello_osp"


@application.route("/")
def hello():
    return render_template("index.html")


@application.route("/login")
def login():
    return render_template("login_.html")


@application.route("/signup")
def signup():
    return render_template("sign_up.html")


@application.route("/signup_post", methods=['POST'])
def register_user():
    data = request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login_.html")
    else:
        flash("user id already exist!")
        return render_template("sign_up.html")

    
@application.route("/submit_item")
def reg_item_submit():
    name = request.args.get("name")
    seller = request.args.get("seller")
    addr = request.args.get("addr")
    tel = request.args.get("tel")
    category = request.args.get("category")
    card = request.args.get("card")
    status = request.args.get("status")
    phone = request.args.get("phone")
    print(name, addr, tel, category, card, status, phone)
    return render_template("reg_items.html")


@application.route("/list")
def view_list():
    return render_template("list.html")


@application.route("/review")
def view_review():
    return render_template("review.html")


@application.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")


@application.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")


@application.route("/submit_items_post", methods=['POST']) 
def reg_item_submit_post():
    image_file = request.files["file"]
    image_file.save("static/image/{}".format(image_file.filename))
    data = request.form
    DB.insert_item(data['name'], data, image_file.filename)

    return render_template("submit_item_result.html", data=data, img_path = "static/images/{}".format(image_file.filename))


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
