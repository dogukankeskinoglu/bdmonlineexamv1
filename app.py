import sys

import flask_login
import uuid
from flask import Flask, request, render_template, redirect, url_for, jsonify, json
from flask_login import LoginManager, login_required, current_user


login_manager = LoginManager()
app = Flask(__name__)

users = {'sakiratsui': {'password': 'secret'}, 'dogukan': {'password': '1234'}}
exams = []
createdexams=[] #tıklandıktan sonra kaydedilmeleri için


# db'den çekilecek

class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return "bad request"

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    name = request.form.get('name')
    if name not in users:
        return "bad request"

    user = User()
    user.id = name
    user.is_authenticated = request.form['password'] == users[name]['password']

    return user


@app.route("/")
def redirecthome():
    return redirect(url_for("login"))


@app.route("/home")
def login():
    return render_template('home.html')  # userexists=current_user , user varsa tekrar login kısmını göstermesin!.


@app.route("/home", methods=["POST"])
def logon():
    name = request.form.get("name")
    if request.form.get("password") == users[name]["password"]:
        usr = User()
        usr.id = name
        flask_login.login_user(usr)
        return redirect(url_for("show_exams"))
    # bu değerler db'de bir veriyle eşleşirse home'a gidilir.
    # else return login again?
    else:
        return "<script> alert('Wrong username or password!'); </script>" + render_template("home.html")


@app.route("/exams", methods=["GET", "POST"])
@login_required
def show_exams():
    if request.method == "POST":
        examdetails = json.loads(request.data)
        # sınav detayları ve adı tarihi db'ye kaydedilecek
        createdexams.append(exams[-1])
        print(createdexams, sys.stdout.flush())
        print(uuid.uuid4(), sys.stdout.flush()) #sınavın unique id'si
    user_type = "öğretmen"  # db'den kullanıcının user type'ı check edilmeli
    return render_template("exams.html", user_type=user_type, exam=createdexams)
    #exam değeri db'den alınacak?


@app.route("/createexam")
@login_required
def create_exam():
    return render_template("createexam.html")


@app.route("/createexam/p=2")
@login_required
def exampagetwo():
    examname = request.args.get("examname")
    start = request.args.get("examstart")
    end = request.args.get("examend")
    exams.append([examname, start, end])
    # alınan değerler db'ye kaydedilecek!
    return render_template("pagetwo.html", examname=examname, start=start, end=end)


@app.route("/leaderboard")
@login_required
def leaderboard():
    names = "dogukan", "muge"  # db.get öğrenci sınav tablosundaki kullanıcı adları
    points = 90, 95  # db.get öğrencisınav tablosundaki notlar
    point_info = zip(names, points)  # ikili tuple'lar haline getirdi.
    point_info = sorted(point_info, key=lambda tup: (-tup[1]))  # tuple'ı notlara göre yüksekten düşüğe sıralama
    return render_template("leaderboard.html", point=point_info)


@app.route("/logout")
@login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.secret_key = 'j1i5ek0eeg+lb0uj^rvm)d1a@qvz^l&1(ep8f54n(oe+uc6s)4'
    login_manager.init_app(app)

    app.run(debug=True)
