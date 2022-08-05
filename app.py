import pandas as pd
import pymongo
from flask import Flask, request, render_template, flash, redirect, url_for, send_file, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/test123"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'pravingohil'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

db_connect = pymongo.MongoClient("mongodb://localhost:27017")
db = db_connect["test_db"]  # database get
collection = db["col1"]


@app.route("/", methods=["GET", "POST"])
def create():  # used to create user and  store data to the mongoDB!!!
    if request.method == "POST":
        username = request.form["username"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        all_database = db_connect.list_databases_names  # just for the got the database details.

        dict1 = {"username": username, "first_name": first_name, "last_name": last_name, "email": email,
                 "password1": password1, "password2": password2}
        # db.products.insertMany( [
        # { item: "card", qty: 15 },
        # { item: "envelope", qty: 20 },                 #it is used for insert many data !!!!
        # { item: "stamps" , qty: 30 }
        # ] );
        collection.insert_one(dict1)

    return render_template("demo.html")


@app.route("/update")
# @app.route("/")                                        # both url are valid.
def update():
    # username = username
    username = request.args.get('username')
    # collections(table )get
    # a = db.col1.find({'username': username})
    myquery = {'username': username}
    new_value = {"$set": {"email": " cjrfrfygvb@gmail.com"}}
    collection.update_one(myquery, new_value)
    return render_template("demo.html")


@app.route("/del")
def delete():  # function used to delete user from the mongoDB !!!!
    username = request.args.get('username')
    collection.delete_one({'username': username})
    return render_template("demo.html")


@app.route("/read")
def read():  # function used to read user data from the mongoDB !!!!
    username = request.args.get('username')
    x = collection.find_one({"username": username})
    x["_id"] = str(x["_id"])
    return x


@app.route("/download")
def down():  # function used to get data from mongoDB and store it to csv file and download it !!!
    username = request.args.get('username')
    # x = collection.find()
    # print(type(x),x)
    x = collection.find_one({'username': username})
    df = pd.DataFrame([x])
    df.to_csv("friend.csv")
    path = r'C:\Users\pravinsinh.gohil\Desktop\pravin flask\friend.csv'
    return send_file(path, as_attachment=True)


@app.route("/sfile")
def index():  # render html file ,we used static file in html .
    return render_template("new.html")


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


@app.route("/reg/", methods=["GET", "POST"])
def register():
    print(request.method)
    if request.method == "POST":
        username = request.form.get("username")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        user = User(username=username, firstname=first_name, lastname=last_name, email=email, password=password1)
        db.session.add(user)
        db.session.commit()
        flash("user registered successfully", "success")
        return redirect('/reg/')
    else:
        return render_template("register.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/loginuser", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username1 = request.form.get("username")
        password1 = request.form.get("password")
        user = User.query.filter_by(username=username1).first()
        print(user)
        if user and password1 == user.password:
            login_user(user)
            flash("user registered successfully", "success")
            return "user  successfully logged in"
        else:
            flash("invalid credential", "warning")
            return redirect('/reg/')

    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/datadsply/", methods=["GET", "POST"])
def disdata():
    data = User.query.all()
    print(data)
    return render_template("dspdatfromdb.html", data1=data)


@app.route('/cookset', methods=['POST', 'GET'])
def set_cookie():
    # if request.method == 'POST':
    # user = request.form['nm']
    # resp = make_response(render_template('new.html'))
    resp = make_response("here is cookie ")
    resp.set_cookie('userID', "pravin")
    return resp


@app.route('/cookget')
def get_cookie():
    name = request.cookies.get('userID')
    return '<h1>welcome ' + name + '</h1>'


@app.route('/visitcount')
def count():
    # count1 = int(request.cookies.get('visit_cookie',0))
    getvalue = int(request.cookies.get("visit_cookie"))
    getvalue = getvalue + 1
    msg = "visited this page " + str(getvalue)
    resp = make_response(msg)
    resp.set_cookie("visit_cookie", str(getvalue))
    return resp


if __name__ == "__main__":
    app.run(debug=True, port=5000)

# app.config["MONGO_URI"] = "mongodb://localhost:27017"
# mongo = PyMongo(app)
# app.config["MONGO_URI"] = False
# mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/todo_db")
# db = mongodb_client.db
#
# @app.route("/add_one")
# def add_one():
#     db.todos.insert_one({'title': "todo title", 'body': "todo body"})
#     return flask.jsonify(message="success")
# app.config["MONGO_URI"] = "mongodb://localhost:27017/todo_db"
# mongodb_client = PyMongo(app)
# db = mongodb_client.db
