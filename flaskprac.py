from flask import Flask, request, render_template, flash, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user,UserMixin,logout_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/test123"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'pravingohil'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, nullable=False)
    firstname = db.Column(db.String(), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username


@app.route("/reg/", methods=["GET", "POST"])
def regi():
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


@app.route("/login", methods=["GET", "POST"])
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
            flash("invalid credential","warning")
            return redirect('/reg/')

    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for( "login"))                   #
    # return "you are logged out successfully"


@app.route("/disdata/", methods=["GET", "POST"])
def disdata():
    data=User.query.all()
    print(data)
    return render_template("dspdatfromdb.html",data1=data)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
