from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
from flask import jsonify
from math import ceil

import hashlib
import sys

application = Flask(__name__)
application.config["SECRET_KEY"] = "hello_osp"


DB = DBhandler()


@application.route("/")
def hello():
    return render_template("index.html")

# 메인 페이지
@application.route("/mainpage")
def mainpage():
    return render_template("mainpage.html")
    
# 회원가입
@application.route("/signup")
def signup():
    return render_template("sign_up.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    password = request.form['password']
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    DB.insert_user(data, pw_hash)

    return render_template("login.html")

    
@application.route("/check_id", methods=['POST'])
def check_duplicate():
    data = request.get_json()
    if data and 'id' in data:
        id = data['id']
        if DB.user_duplicate_check(id):
            return jsonify({'message': 'ID available'}), 200
        else:
            return jsonify({'message': 'ID already exists'}), 409
    else:
        return jsonify({'message': 'Invalid data format'}), 400


# 로그인
@application.route("/login")
def login():
    return render_template("login.html")

@application.route("/login_confirm", methods=['POST']) 
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest() 
    if DB.find_user(id_ ,pw_hash):
        session['id'] = id_
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html")

# 로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))


# 세션 체크
@application.route("/check-session")
def check_session():
    user_id = session.get('id')
    return jsonify(isLoggedIn=bool(user_id), userId=user_id)


# 상품 등록
@application.route("/reg_items", methods=['GET', 'POST']) 
def reg_item():
    return render_template("reg_items.html")


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
        data['img_path'] = '../static/images/' +  file.filename
    
    DB.insert_item(data['product-name'], data)
    return render_template("submit_item_result.html", data=data)


# 상품 전체 조회
@application.route("/list")
def view_list():
    items = DB.get_all_items()
    items_per_page = 6
    total_pages = (len(items) + items_per_page - 1) // items_per_page  # 페이지 수 계산
    return render_template('item.html', items=items, totalPages=total_pages, currentPage = 1, itemsPerPage = 6)


# 상품 상세 조회
@application.route("/view_detail/<name>/") 
def view_item_detail(name):
    print("###name:",name)
    data = DB.get_item_byname(str(name)) 
    print("####data:",data)
    return render_template("items_detailed.html", name=name, data=data)


# 좋아요 조회

@application.route('/show_heart/<name>/', methods=['GET'])
def show_heart(name):
    my_heart = DB.get_heart_byname(session['id'],name)
    return jsonify({'my_heart': my_heart})


# 좋아요 등록
@application.route('/like/<name>/', methods=['POST'])
def like(name):
    my_heart = DB.update_heart(session['id'],'Y',name)
    return jsonify({'msg': '좋아요 완료!'})


# 안좋아요 등록
@application.route('/unlike/<name>/', methods=['POST'])
def unlike(name):
    my_heart = DB.update_heart(session['id'],'N',name)
    return jsonify({'msg': '안좋아요 완료!'})


# 리뷰 등록
@application.route("/reg_review_init/<name>/") 
def reg_review_init(name):
    return render_template("reg_reviews.html", name=name)

@application.route("/reg_review", methods=['POST']) 
def reg_review():
    data = {
        "title": request.form.get('reviewTitle'),
        "point": request.form.get('rating'),
        "content": request.form.get('reviewText'),
        "authorId": request.form.get('reviewerId'),
        "productName": request.form.get('productName')
    }
    if 'productImage' in request.files:
        file = request.files['productImage']
        # 파일을 어디에 저장할지 결정하고 저장합니다.
        img_path = "./static/images/" + file.filename
        file.save(img_path)
        data['img_path'] = '../static/images/' + file.filename
    
    DB.reg_review(data)
    return redirect(url_for('view_review'))


# 리뷰 전체 조회
@application.route("/review")
def view_review():
    page = request.args.get("page", 0, type=int)
    per_page = 3  # 페이지 당 표시할 리뷰 수
    start_idx = per_page * page
    end_idx = start_idx + per_page
    data = DB.get_all_reviews()  # 리뷰 데이터 가져오기
    item_counts = len(data)
    page_count = ceil(item_counts / per_page)  # 올림 처리하여 페이지 수 계산
    data = dict(list(data.items())[start_idx:end_idx])  # 현재 페이지에 해당하는 데이터 슬라이싱

    # 페이지에 표시할 리뷰 데이터를 템플릿으로 전달
    return render_template(
        "review_overview.html",
        reviews=data.items(),
        page=page,
        page_count=page_count,
        total=item_counts
    )



# 리뷰 상세 조회
@application.route("/review_detail/<name>/")
def view_review_detail(name):
    review_data = DB.get_review_byname(name)
    print(review_data)
    return render_template("review_detailed.html", review=review_data)



if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
