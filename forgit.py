from flask_mail import Mail, Message
import pandas as pd
import pymongo
from flask import Flask, request, render_template, flash, redirect, url_for, send_file, make_response, jsonify, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, UserMixin, logout_user

app = Flask(__name__)
# logging.basicConfig(filename='demo.log', level=logging.DEBUG)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/test123"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'pravingohil'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/", methods=["GET", "POST"])
def create():  # used to create user and  store data to the mongoDB!!!
    if request.method == "POST":
        username = request.form["username"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        db_connect = pymongo.MongoClient("mongodb://localhost:27017")  # connect to the database
        db = db_connect["test_db"]  # get database
        collection = db["col1"]  # get collections(table )

        dict1 = {"username": username, "first_name": first_name, "last_name": last_name, "email": email,
                 "password1": password1, "password2": password2}
        # db.products.insertMany( [
        # { item: "card", qty: 15 },
        # { item: "envelope", qty: 20 },                                #it is used for insert many data !!!!
        # { item: "stamps" , qty: 30 }
        # ] );
        collection.insert_one(dict1)

    return render_template("demo.html")


@app.route("/update")
# @app.route("/")                                                   #both url are valid.
def update():
    # username = username
    username = request.args.get('username')  # demo url ......"http://127.0.0.1:5005/update?username=vijay"
    db_connect = pymongo.MongoClient("mongodb://localhost:27017")
    db = db_connect["test_db"]  # database get
    collection = db["col1"]  # collections(table )get

    myquery = {'username': username}
    new_value = {"$set": {"email": " cjrfrfygvb@gmail.com"}}
    collection.update_one(myquery, new_value)
    return render_template("demo.html")


@app.route("/del")
def delete():  # function used to delete user from the mongoDB !!!!
    username = request.args.get('username')
    db_connect = pymongo.MongoClient("mongodb://localhost:27017")
    db = db_connect["test_db"]
    collection = db["col1"]
    collection.delete_one({'username': username})
    return render_template("demo.html")


@app.route("/read")
def read():  # function used to read user data from the mongoDB !!!!
    username = request.args.get('username')
    db_connect = pymongo.MongoClient("mongodb://localhost:27017")
    db = db_connect["test_db"]
    collection = db["col1"]
    x = collection.find_one({"username": username})
    if username:
        x["_id"] = str(x["_id"])
        app.logger.info('Info level log')
        return x
    app.logger.info('Info level log')
    return "user is non"


@app.route("/downloader")
def down():  # function used to get data from mongoDB and store it to csv file and  automatically download it !!!
    username = request.args.get('username')
    db_connect = pymongo.MongoClient("mongodb://localhost:27017")
    db = db_connect["test_db"]
    collection = db["col1"]
    x = collection.find_one({'username': username})
    df = pd.DataFrame([x])
    df.to_csv("friend.csv")
    path = r'C:\Users\pravinsinh.gohil\Desktop\pravin flask\friend.csv'
    return send_file(path, as_attachment=True)


@app.route("/static_file")
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
def register():  # user can fill their details for registration
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


@app.route("/login_user", methods=["GET", "POST"])
def login():  # function used for login ,
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


@app.route("/log_out")
def logout():
    # logout_user()

    print(session.pop('username', None))

    return redirect(url_for("login"))


# -----------------------------------------------------------------------------------------------
# 22/07 reviewed


@app.route("/data_dsply/", methods=["GET", "POST"])
def disdata():  # get data from database and display it to the frontend.
    data = User.query.all()
    print(data)
    return render_template("dspdatfromdb.html", data1=data)


@app.route('/cook_set', methods=['POST', 'GET'])
def set_cookie():  # used for set cookie
    resp = make_response("ubyjhmjjhkj,hyjyvyvyu")
    resp.set_cookie('userID', "pravin")
    return resp


@app.route('/cook_get')
def get_cookie():  # used for get cookie
    name = request.cookies.get('userID')
    return '<h1>welcome ' + name + '</h1>'


@app.route('/visit_count')
def count():  # function used for  count user visit
    getvalue = int(request.cookies.get("visit_cookie"))
    getvalue = getvalue + 1
    msg = "visited this page " + str(getvalue)
    resp = make_response(msg)
    resp.set_cookie("visit_cookie", str(getvalue))
    return resp


def about():
    db_connect = pymongo.MongoClient("mongodb://localhost:27017")
    db = db_connect["test_db"]
    collection = db["col1"]
    abc=db.col1.find({"username":"jaydip"})
    print(abc)
    x = collection.find_one({'username': "vijay"})
    if x:
        x["_id"] = str(x["_id"])
        return jsonify(x)
    else:
        return "username not  available "


app.add_url_rule("/about", "about", about)


@app.route('/file_upload')
def upload():
    return render_template("file_upload.html")


@app.route('/store', methods=['GET', 'POST'])
def store_file():
    if request.method == 'POST':
        f = request.files['file']
        print(type(f))
        f.save('C:/Users/pravinsinh.gohil/Desktop/file_uploding/yh.jpg')
        # app.logger.info('Info level log')
    return redirect(url_for("upload"))


@app.route('/home/<string:name>')
def home(name):
    return "hello," + name


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'p.gohil1111@gmail.com'
app.config['MAIL_PASSWORD'] = 'dlkfsjgdlkfjhfdhj'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route("/mails")
def index1():
    msg = Message('Hello', sender='p.gohil1111@gmail.com', recipients=['harsh.thakkar@msbcgroup.com'])
    msg.body = "hello harsh how are you bro ?"
    mail.send(msg)
    return "Sent"


if __name__ == "__main__":
    app.run(debug=True, port=5005)
