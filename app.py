import sys
import flask_login
import uuid
from flask import Flask, request, render_template, redirect, url_for, jsonify, json
from flask_login import LoginManager, login_required, current_user
from psycopg2._psycopg import cursor
from database import Database
login_manager = LoginManager()
app = Flask(__name__)
login_manager.init_app(app)
login_manager.login_view = 'login'
#users = {'sakiratsui': {'password': 'secret'}, 'dogukan': {'password': '1234'}}
exams = []
createdexams = []  # tıklandıktan sonra kaydedilmeleri için
# db'den çekilecek
class User(flask_login.UserMixin):
    def __init__(self, username, password, usertype):
        self.username = username
        self.password = password
        self.usertype = usertype
@login_manager.user_loader
def user_loader(username):
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Kullanici WHERE kullanici_adi= %s", (username,))
        rows = cursor.fetchall()
        if username not in rows:
            return "bad request"
        user = User()
        user.username = username
    return user
@login_manager.request_loader
def request_loader(request):
    name = request.form.get('name')
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Kullanici WHERE kullanici_adi= %s", (name,))
        rows = cursor.fetchall()
        if name not in rows:
            return "bad request"
        user = User()
        user.username = name
        user.is_authenticated = request.form['password'] == rows[2]
    return user
@app.route("/")
def redirecthome():
    return redirect(url_for("login"))

@app.route("/home", methods=["POST","GET"])
def login():
    if request.method=="POST":
        name = request.form.get("name")
        db = Database()
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM Kullanici WHERE kullanici_adi= %s", (name,))
            rows = cursor.fetchall()
            for row in rows:
                if request.form.get("password") == str(row[2]):
                    usr = User()
                    usr.username = name
                    usr.password = str(row[2])
                    usr.usertype = str(row[3])
                    flask_login.login_user(usr)
                    return render_template("exams.html", user_type=usr.usertype, exam=createdexams)
                else:
                    return "<script> alert('Wrong username or password!'); </script>" + render_template("home.html")
    return render_template("home.html")
    # bu değerler db'de bir veriyle eşleşirse home'a gidilir.
    # else return login again?
@app.route("/exams", methods=["GET", "POST"])
@login_required
def show_exams():
    if request.method == "POST":
        examdetails = json.loads(request.data)
        # created exams ve exam details parse edilip eklenecek
        createdexams.append(exams[-1])
        print(createdexams, sys.stdout.flush())
    # Sınav(sınav_id,sinav_adi,sınav_baslama,sınav_bitis)
        db = Database()
        with db.get_cursor() as cursor:
            cursor.execute("INSERT INTO Sinav(sinav_adi,sinav_baslama_tarihi,sinav_bitis_tarihi) VALUES (%s, %s,%s);",
                       (exams[-1][0], exams[-1][1], exams[-1][2]))
        db.commit()
    return render_template("exams.html", user_type="Ogretmen", exam=createdexams)