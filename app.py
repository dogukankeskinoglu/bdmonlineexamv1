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
exams = []
current_usertype="Ogrenci"
current_user_id=0
sinav_id=0
sinav_toplam_puan=0
sinav_ham_puan=0
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
                    global current_usertype
                    global current_user_id
                    current_user_id=row[0]
                    current_usertype = str(row[3])
                    return redirect(url_for("show_exams"))
                else:
                    return "<script> alert('Wrong username or password!'); </script>" + render_template("home.html")
    return render_template('home.html') 


@app.route("/exams", methods=["GET", "POST"])
#@login_required
def show_exams():
    createdexams = manage.getExamFromDataBase()
    if request.method == "POST":
        exam_number=Exam.exam_count+1
        exam_object=Exam(exam_number,current_user_id,exams[-1][0], exams[-1][1], exams[-1][2])
        createdexams.append(exam_object)
        manage.insertExamDataBase(exam_object)
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
    return render_template("exams.html", user_type=current_usertype, exam=createdexams)

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
                            sorusayisi=soru_sayisi,
                            soruid=soru_id
                          )

          
@app.route("/exam/examresult", methods=["POST","GET"])
def exam_result():
    if request.method=="POST":
       global sinav_id
       global sinav_toplam_puan
       global sinav_ham_puan
       resultdetails = json.loads(request.data)
       penalty=1.25
       ogrenci_puan=0
       sinav_id=manage.getExamId(resultdetails["data"][0]["key"])
       sinav_bitiris_tarihi=resultdetails["data"][0]["value"]["bitis_zamani"]
       sinav_toplam_puan=manage.getExamTotalPoint(int(sinav_id))
       sinav_soru_sayisi=len(resultdetails["data"])
       soru_agirlik=[0]*sinav_soru_sayisi
       liste=[0]*sinav_soru_sayisi
       for index,i in enumerate(resultdetails["data"]):
           sorudan_aldigi_puan=0
           isaretlenen_=i["value"]["isaretlenen"]
           soru_id=i["key"]
           soru_bilgiler=manage.getQuestionPoint(soru_id)
           dogru_cevap=soru_bilgiler[0]
           soru_puan=soru_bilgiler[1]
           if dogru_cevap==isaretlenen_:
               liste[index]=1
               sorudan_aldigi_puan=soru_puan
               sinav_ham_puan+=sorudan_aldigi_puan
           else:
                soru_agirlik[index]=(soru_puan/sinav_toplam_puan)*penalty
           manage.insertStudentQuestionDataBase(current_user_id,soru_id,isaretlenen_,sorudan_aldigi_puan)
       toplam_ceza=sum(soru_agirlik)
       ogrenci_puan=sinav_toplam_puan-(toplam_ceza*sinav_toplam_puan)
       if (ogrenci_puan<0):
           ogrenci_puan=0
       dogru_cevap_sayisi=liste.count(1)
       yanlis_cevap_sayisi=liste.count(0)
       manage.insertStudentExamDatabase(current_user_id,sinav_id,sinav_bitiris_tarihi,dogru_cevap_sayisi,yanlis_cevap_sayisi,ogrenci_puan)
    ogrenci_result=manage.getStudentExamResult(current_user_id,sinav_id)
    return render_template("show_exam_result.html",ogrenci_id=ogrenci_result[0],
                        sinav_id=ogrenci_result[1],
                        sinav_bitiris_tarihi=ogrenci_result[2],
                        dogru_cevap=ogrenci_result[3],
                        yanlis_cevap=ogrenci_result[4],
                        ogrenci_puan=ogrenci_result[5],
                        sinav_toplam_puan=sinav_toplam_puan,
                        sinav_ham_puan=sinav_ham_puan)
    


@app.route("/createexam/p=2")
#@login_required
def exampagetwo():
    examname = request.args.get("examname")
    start = request.args.get("examstart")
    end = request.args.get("examend")
    exams.append([examname, start, end])
    return render_template("pagetwo.html", examname=examname, start=start, end=end)


@app.route("/leaderboard")
def exam_leaderboard():
    if current_usertype=="Ogretmen":
        ogretmen_sinavlari=manage.getTeacherExam(current_user_id)
        return render_template("sinavleaderboard.html",sinav=ogretmen_sinavlari,tip=current_usertype)
    else:
        ogrenci_sinavlari=manage.getStudentExam(current_user_id)
        return render_template("sinavleaderboard.html",sinav=ogrenci_sinavlari,tip=current_usertype)
    

@app.route("/leaderboard/<exam_id>")
#@login_required
def leaderboard(exam_id):
    liste=manage.getLeaderBoardExam(exam_id)
    return render_template("leaderboard.html",leadorboard=liste)


@app.route("/logout")
#@login_required
def logout():
    #flask_login.logout_user()
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.secret_key = 'j1i5ek0eeg+lb0uj^rvm)d1a@qvz^l&1(ep8f54n(oe+uc6s)4'
    app.run(debug=True)


