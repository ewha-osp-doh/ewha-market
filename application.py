from flask import Flask, render_template

application = Flask(__name__)


@application.route("/")
def hello():
    return render_template("index.html")


@application.route("/submit_item")
def reg_item_submit():
    name=request.args.get("name")
    seller=request.args.get("seller") 
    addr=request.args.get("addr") 
    email=request.args.get("email") 
    category=request.args.get("category") 
    card=request.args.get("card") 
    status=request.args.get("status") 
    phone=request.args.get("phone")
    print(name,addr,tel,category,park,time,site) 
    return render_template("reg_item.html")

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=False)