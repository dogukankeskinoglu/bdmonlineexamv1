import sys
import psycopg2
import flask_login
import uuid
from flask import Flask, request, render_template, redirect, url_for, jsonify, json
#from flask_login import LoginManager, login_required, current_user

from database import Database

#login_manager = LoginManager()

app = Flask(__name__)
#login_manager.init_app(app)
#login_manager.login_view = 'login'

# users = {'sakiratsui': {'password': 'secret'}, 'dogukan': {'password': '1234'}}

exams = []
createdexams = []  # tıklandıktan sonra kaydedilmeleri için


# db'den çekilecek

class User(flask_login.UserMixin):
    def __init__(self, username, password, usertype):
        self.username = username
        self.password = password
        self.usertype = usertype


class User(flask_login.UserMixin):
    pass


@app.route("/")
def redirecthome():
    return redirect(url_for("login"))


@app.route("/home",methods=["GET","POST"])
def login():
    if request.method=="POST":
        name = request.form.get("name")
        print(name,sys.stdout.flush())
        db = Database()
        print("sa",sys.stdout.flush())
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM Kullanici WHERE kullanici_adi= %s", (name,))
            rows = cursor.fetchall()
            for row in rows:
                if request.form.get("password") == str(row[2]):
                    #return  "success"
                    return redirect(url_for("show_exams"))
                else:
                    return "<script> alert('Wrong username or password!'); </script>" + render_template("home.html")
    return render_template('home.html')  # userexists=current_user , user varsa tekrar login kısmını göstermesin!.




@app.route("/exams", methods=["GET", "POST"])
#@login_required
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


@app.route("/createexam")
#@login_required
def create_exam():
    return render_template("createexam.html")


@app.route("/createexam/p=2")
#@login_required
def exampagetwo():
    examname = request.args.get("examname")
    start = request.args.get("examstart")
    end = request.args.get("examend")
    exams.append([examname, start, end])
    return render_template("pagetwo.html", examname=examname, start=start, end=end)


@app.route("/leaderboard")
#@login_required
def leaderboard():
    names = "dogukan", "muge"  # db.get öğrenci sınav tablosundaki kullanıcı adları
    points = 90, 95  # db.get öğrencisınav tablosundaki notlar
    point_info = zip(names, points)  # ikili tuple'lar haline getirdi.
    point_info = sorted(point_info, key=lambda tup: (-tup[1]))  # tuple'ı notlara göre yüksekten düşüğe sıralama
    return render_template("leaderboard.html", point=point_info)


@app.route("/logout")
#@login_required
def logout():
    #flask_login.logout_user()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.secret_key = '!$w4wW~o|~8OVFX'
    app.run(debug=True)
