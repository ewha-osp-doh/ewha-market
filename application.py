from flask import Flask, render_template, request, flash, redirect, url_for, session
from database import DBhandler

import hashlib
import sys


application = Flask(__name__)
application.config["SECRET_KEY"] = "hello_osp"


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
    data = {
        "seller-id" : request.form.get("sellerId"),
        "product-name" : request.form.get("productName"),
        "product-price" : request.form.get("productPrice"),
        "product-status" : request.form.get("condition"),
        "product-description" : request.form.get("productDescription")
    }
    DB.insert_item(data['product-name'], data)
    return render_template("submit_item_result.html", data=data)

@application.route("/login")
def login():
    return render_template("login.html")


@application.route("/login_confirm", methods=['POST']) 
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest() 
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")

@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

@application.route("/signup")
def signup():
    return render_template("Signup.html")


@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw = request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("Signup.html")

@application.route("/check-session")
def check_session():
    user_id = session.get('id')
    return jsonify(isLoggedIn=bool(user_id), userId=user_id)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
