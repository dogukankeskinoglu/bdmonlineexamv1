import sys
from templates.exam import Exam
from templates.question import Question
import flask_login
import uuid
from flask import Flask, request, render_template, redirect, url_for, jsonify, json
from flask_login import login_required
from psycopg2._psycopg import cursor
import manage
from database import Database
app = Flask(__name__)
#users = {'sakiratsui': {'password': 'secret'}, 'dogukan': {'password': '1234'}}
exams = []
createdexams = manage.getExamFromDataBase() # tıklandıktan sonra kaydedilmeleri için
# db'den çekilecek
class User(flask_login.UserMixin):
    def __init__(self, username, password, usertype):
        self.username = username
        self.password = password
        self.usertype = usertype


@app.route("/")
def redirecthome():
    return redirect(url_for("login"))

@app.route("/home", methods=["POST","GET"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        db = Database()
        with db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM Kullanici WHERE kullanici_adi= %s", (name,))
            rows = cursor.fetchall()
            for row in rows:
                if request.form.get("password") == str(row[2]):
                    usertype = str(row[3])
                    return render_template("exams.html", user_type=usertype, exam=createdexams)
                else:
                    return "<script> alert('Wrong username or password!'); </script>" + render_template("home.html")
    return render_template('home.html') 


@app.route("/exams", methods=["GET", "POST"])
#@login_required
def show_exams():
    if request.method == "POST":
        exam_number=Exam.exam_count+1
        exam_object=Exam(exam_number,exams[-1][0], exams[-1][1], exams[-1][2])
        createdexams.append(exam_object)
        manage.insertExamDataBase(exam_object)
        print(createdexams, sys.stdout.flush())
        examdetails = json.loads(request.data)
        exam_id=manage.getExam(exam_object.exam_name)
        for i in examdetails["data"]:
            question=i["value"]["question"]
            a_choice=i["value"]["a_choice"]
            b_choice=i["value"]["b_choice"]
            c_choice=i["value"]["c_choice"]
            d_choice=i["value"]["d_choice"]
            e_choice=i["value"]["e_choice"]
            true_answer_choice=i["value"]["true_answer_choice"]
            question_point=int(i["value"]["question_point"])
            all_choice=a_choice+"*_*"+b_choice+"*_*"+c_choice+"*_*"+d_choice+"*_*"+e_choice
            manage.insertQuestionDataBase(exam_id,question,all_choice,true_answer_choice,question_point)
    return render_template("exams.html", user_type="Ogretmen", exam=createdexams)



@app.route("/createexam")
#@login_required
def create_exam():
    return render_template("createexam.html")

@app.route("/exam/<exam_id>")
def nolr(exam_id):
    sorular=manage.getQuestion(exam_id)
    soru_sayisi=len(sorular)
    soru_id=[]
    soru_dogru_cevap=[]
    soru_puan=[]
    for i in sorular:
        soru_id.append(i[0])
        soru_dogru_cevap.append(i[4])
        soru_puan.append(i[5])
    return render_template("showquestion.html",
                            examid=exam_id,
                            sorular=sorular,
                            sorusayisi=soru_sayisi
                          )

                        
@app.route("/exam/examresult", methods=["POST","GET"])
def exam_result():
    resultdetails=[]
    if request.method=="POST":
        resultdetails = json.loads(request.data)
        return render_template("show_exam_result.html",result=resultdetails)
    return render_template("show_exam_result.html",result=resultdetails)


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
    app.secret_key = 'j1i5ek0eeg+lb0uj^rvm)d1a@qvz^l&1(ep8f54n(oe+uc6s)4'
    app.run(debug=True)