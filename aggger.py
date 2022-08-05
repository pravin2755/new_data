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


@app.route("/update")
# @app.route("/")                                                   #both url are valid.
def update():
    # username = username
    username = request.args.get('username')  # demo url ......"http://127.0.0.1:5005/update?username=vijay"
    db_connect = pymongo.MongoClient("mongodb://localhost:27017")
    db = db_connect["test_db"]  # database get
    da=db.col1.find()
    print(da)
    for i in da:
        print(i)
    return "sucess"


if __name__ == "__main__":
    app.run(debug=True, port=5010)
