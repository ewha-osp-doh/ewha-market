from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler

import hashlib
import sys


application = Flask(__name__)
application.config["SECRET_KEY"] = "hello_osp"


DB = DBhandler()


@application.route("/")
def hello():
    return render_template("index.html")

# 회원가입
@application.route("/signup")
def signup():
    return render_template("sign_up.html")

@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    password = request.form['password']
    pw_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html")
    else:
        flash("user id already exist!")
        return render_template("sign_up.html")

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

@application.route("/sign_up")
def view_sign_up():
    return render_template("sign_up.html")


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
    per_page=6 # item count to display per page
    per_row=3# item count to display per row
    row_count=int(per_page/per_row)
    start_idx=per_page*page
    end_idx=per_page*(page+1)
    data = DB.get_all_reviews() #read the table
    item_counts = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    tot_count = len(data)
    for i in range(row_count):#last row
        if (i == row_count-1) and (tot_count%per_row != 0):
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:])
        else: 
            locals()['data_{}'.format(i)] = dict(list(data.items())[i*per_row:(i+1)*per_row])
    return render_template(
        "review_overview.html",
        datas=data.items(),
        row1=locals()['data_0'].items(),
        row2=locals()['data_1'].items(),
        limit=per_page,
        page=page,
        page_count=int((item_counts/per_page)+1),
        total=item_counts)


# 리뷰 상세 조회
@application.route("/review_detail/<name>/")
def view_review_detail(name):
    review_data = DB.get_review_byname(name)
    print(review_data)
    return render_template("review_detailed.html", review=review_data)


# 마이페이지
@application.route("/mypage")
def view_mypage():
    #회원정보
    
    #구매내역
    
    #등록내역
    registered_item = DB.get_users_registered_item(session['id'])
    print(registered_item)
    return render_template("mypage.html", registered=registered_item)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)