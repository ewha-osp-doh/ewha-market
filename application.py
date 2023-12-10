from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from database import DBhandler
from flask import jsonify

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
    return redirect(url_for('login'))


# 세션 체크
@application.route("/check-session")
def check_session():
    user_id = session.get('id')
    return jsonify(isLoggedIn=bool(user_id), userId=user_id)


# 상품 등록
@application.route("/reg_items", methods=['GET', 'POST']) 
def reg_item():
    return render_template("reg_items.html", user=session['id'])


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
    return redirect('/view_detail/'+data['product-name'])


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
    return render_template("reg_reviews.html", name=name, user=session['id'])

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


#리뷰 전체 조회
@application.route("/review")
def view_review():
    # 페이지 번호 처리 (1부터 시작)
    page = request.args.get("page", 1, type=int)
    per_page = 3  # 페이지 당 리뷰 수
    per_row = 3  # 행 당 리뷰 수

    data = DB.get_all_reviews()  # DB에서 리뷰 가져오기
    item_counts = len(data)

    # 1부터 시작하는 페이지 번호를 0부터 시작하는 인덱스로 변환
    start_idx = per_page * (page - 1)
    end_idx = start_idx + per_page
    data = dict(list(data.items())[start_idx:end_idx])

    # 페이지 당 표시할 리뷰 처리 및 리뷰 등록자 아이디 처리
    row_data = {}
    for i in range(per_page):
        if i * per_row < len(data):
            row_key = 'data_{}'.format(i)
            row_items = dict(list(data.items())[i * per_row:(i + 1) * per_row])

            # 각 리뷰 아이템에 대해 등록자 아이디 처리
            for key, value in row_items.items():
                author_id = value['authorId']
                # 첫 두 글자를 제외한 나머지를 *로 대체
                masked_id = author_id[:2] + '*' * (len(author_id) - 2)
                value['authorId'] = masked_id
            
            row_data[row_key] = row_items.items()

    # 페이지네이션을 위한 페이지 수 계산
    page_count = (item_counts // per_page) + (1 if item_counts % per_page else 0)
    return render_template(
        "review_overview.html",
        int=int,
        page=page,
        row_data=row_data,
        current_page=page,
        page_count=page_count,
        total=item_counts
    )


# 리뷰 상세 조회
@application.route("/review_detail/<name>/")
def view_review_detail(name):
    review_data = DB.get_review_byname(name)
    print(review_data)
    return render_template("review_detailed.html", review=review_data)


# 마이페이지
@application.route("/mypage")
def view_mypage():
    user_id = session['id']
    
    #회원정보
    user_info = DB.get_user_info(user_id)
    
    #좋아요 내역
    user_like = DB.get_top_2_hearts_byname(user_id)
    print(user_like[0])

    #등록내역
    registered_item = DB.get_users_registered_item(user_id)
    print(registered_item)
    return render_template("mypage.html", user=user_info, user_like = user_like, user_register=registered_item)


# 회원탈퇴
@application.route("/withdrawal")
def withdraw():
    user_id = session['id']
    DB.withdraw_user(user_id)
    return redirect(url_for('login'))
    # return jsonify({'msg': '탈퇴 완료'})
    
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)
