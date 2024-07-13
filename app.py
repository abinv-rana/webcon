from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import session
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import flash
import datetime


app = Flask(__name__)
app.secret_key = "verysecret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
app.config['SECRET_KET'] = 'verysecret'

database = SQLAlchemy(app)
class articles(database.Model, UserMixin):
    _id = database.Column("id", database.Integer, primary_key= True)
    date = database.Column(database.String(100), nullable = False)
    title = database.Column(database.String(100), nullable = False, unique = True)
    content = database.Column(database.String(1000), nullable = False)

    def __init__(self, date, title, content):
        self.date = date
        self.title = title
        self.content = content

class admin_ids(database.Model):
    _id = database.Column("id", database.Integer, primary_key=True)
    admin_id = database.Column(database.String(100), nullable = False, unique = True)
    password = database.Column(database.String(100), nullable = False)

    def __init__(self, password, admin_id):
        self.admin_id = admin_id
        self.password = password

@app.route("/")
def home():
    value = articles.query.all()
    value_desc = []
    for i in range (len(value)-1, -1, -1):
        value_desc.append(value[i])
    return render_template("home.html", value = value_desc[0])

@app.route("/news/")
def news():
    value = articles.query.all()
    value_desc = []
    for i in range (len(value)-1, -1, -1):
        value_desc.append(value[i])
    return render_template("news.html", value = value_desc)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/admin", methods=["POST", "GET"])
def admin():
    if "admin_id" in session:
        if request.method == "POST":
            date = datetime.datetime.now().date()
            title = request.form["title"]
            content = request.form["content"]
            rep1 = articles.query.filter_by(content=content).first()
            rep = articles.query.filter_by(title=title).first()
            if rep:
                flash("Article with this title already exsits.")
            elif rep1:
                flash("Article with this content already exsists")
            else:
                flash("Article posted succesfully")
                commit = articles(date=date, title=title, content=content)
                database.session.add(commit)
                database.session.commit()


            print(date, title, content)
        return render_template("admin.html")
    else:
        flash("First login as admin",)
        return redirect(url_for("auth"))
    
@app.route("/auth", methods = ["POST", "GET"])
def auth():
    if request.method == 'POST':
        admin_id = request.form['id']
        password = request.form['password']

        adm_id = admin_ids.query.filter_by(admin_id=admin_id).first()

        if adm_id:
            if adm_id.admin_id == admin_id and adm_id.password == password:
                session['admin_id'] = adm_id.admin_id
                session['password'] = adm_id.password
                flash("Login successful")
                return redirect(url_for('admin'))
            else:
                flash('Wrong ID or password', 'error')
                return render_template("auth.html")
        else:
            flash('Wrong ID or password', 'error')
            render_template("auth.html")
    else:
        if 'admin_id' in session:
            return redirect(url_for("admin"))
    return render_template("auth.html")

@app.route("/logout")
def logout():
    flash("You have been logged out!")
    session.pop("admin_id", None)
    return redirect(url_for("home"))

@app.route("/learn")
def learn():
    return render_template("learn.html")
   
@app.route("/learn/ch1")
def ch1():
    return render_template("ch1.html")

@app.route("/learn/ch2")
def ch2():
    return render_template("ch2.html")

@app.route("/learn/ch3")
def ch3():
    return render_template("ch3.html")

@app.route("/learn/ch4")
def ch4():
    return render_template("ch4.html")

@app.route("/learn/ch5")
def ch5():
    flash("Finshed guide.")
    return render_template("ch5.html")


with app.app_context():
    database.create_all()
    app.run(debug=True)