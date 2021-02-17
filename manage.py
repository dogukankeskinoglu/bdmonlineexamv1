import argparse
import os
from os import path
from database import Database
from templates.exam import Exam
from templates.question import Question
parser = argparse.ArgumentParser(description='App manager.')
parser.add_argument('command', metavar="cmd", type=str, help='command to manage the app')

args = parser.parse_args()
sinav_id_sayac=0

import json
#Kullanıcı(kullanici_id,kullanici_adi,kullanici_sifre,kullanici_tipi)
#Sınav(sinav_id,sinav_adi,sinav_baslama_tarihi,sinav_bitis_tarihi)
#Ogrenci_Sınav(ogrenci_id,sinav_id,ogrenci_sinav_bitis_tarihi,dogru_sayi,yanlis_cevap,puan)
#Soru(soru_id,soru_sinav_id,soru_metni,soru_siklari,soru_dogru_cevap,soru_puani)
#Ogrenci_Soru(ogrenci_id,soru_id,verilen_cevap,aldigi_puan)

def create_database():
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("CREATE TABLE Kullanici (kullanici_id serial PRIMARY KEY,kullanici_adi VARCHAR(50) NOT NULL,kullanici_sifre VARCHAR(50) NOT NULL,kullanici_tipi VARCHAR(50) NOT NULL);")
        cursor.execute("CREATE TABLE Sinav(sinav_id serial PRIMARY KEY,ogretmen_id INTEGER,sinav_adi VARCHAR(50) NOT NULL,sinav_baslama_tarihi timestamp  NOT NULL,sinav_bitis_tarihi timestamp NOT NULL,FOREIGN KEY(ogretmen_id) REFERENCES Kullanici(kullanici_id));")
        cursor.execute("CREATE TABLE Soru(soru_id serial PRIMARY KEY,soru_sinav_id INTEGER NOT NULL,soru_metni VARCHAR(100000) NOT NULL,soru_siklari VARCHAR(100000) NOT NULL,soru_dogru_cevap CHAR(1) NOT NULL,soru_puani INTEGER NOT NULL,FOREIGN KEY(soru_sinav_id) REFERENCES Sinav(sinav_id));")
        cursor.execute("CREATE TABLE Ogrenci_Soru(ogrenci_id INTEGER,soru_id INTEGER ,verilen_cevap CHAR(1) NOT NULL,aldigi_puan INTEGER NOT NULL,PRIMARY KEY(ogrenci_id,soru_id),FOREIGN KEY(ogrenci_id) REFERENCES Kullanici(kullanici_id),FOREIGN KEY (soru_id) REFERENCES Soru(soru_id));")
        cursor.execute("CREATE TABLE Ogrenci_Sinav(ogrenci_id INTEGER,sinav_id INTEGER,ogrenci_sinav_bitis_tarihi timestamp NOT NULL,dogru_sayi INTEGER NOT NULL ,yanlis_cevap INTEGER NOT NULL ,puan INTEGER NOT NULL,PRIMARY KEY(ogrenci_id,sinav_id),FOREIGN KEY(ogrenci_id) REFERENCES Kullanici(kullanici_id),FOREIGN KEY(sinav_id) REFERENCES Sinav(sinav_id));")
    db.commit()
    print("Finished creating table")

def fill_database():
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("INSERT INTO Kullanici (kullanici_adi,kullanici_sifre,kullanici_tipi) VALUES (%s, %s, %s);", ("dogukan","public","Ogrenci"))
        cursor.execute("INSERT INTO Kullanici (kullanici_adi,kullanici_sifre,kullanici_tipi) VALUES (%s, %s, %s);", ("mgselen","private","Ogrenci"))
        cursor.execute("INSERT INTO Kullanici (kullanici_adi,kullanici_sifre,kullanici_tipi) VALUES (%s, %s, %s);", ("batuayyildiz","static","Ogrenci"))
        cursor.execute("INSERT INTO Kullanici (kullanici_adi,kullanici_sifre,kullanici_tipi) VALUES (%s, %s, %s);", ("hasanbulut","bulutbilisim","Ogretmen"))
        cursor.execute("INSERT INTO Kullanici (kullanici_adi,kullanici_sifre,kullanici_tipi) VALUES (%s, %s, %s);", ("vecdiaytac","12345","Ogretmen"))
    db.commit()
    print("Inserted 4 rows of data")



def drop_database():
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS Ogrenci_Sinav;")
        cursor.execute("DROP TABLE IF EXISTS Ogrenci_Soru;")
        cursor.execute("DROP TABLE IF EXISTS Soru;")
        cursor.execute("DROP TABLE IF EXISTS Sinav;")
        cursor.execute("DROP TABLE IF EXISTS Kullanici;")
    db.commit()
    print("Finished dropping tables")

def getExamFromDataBase():
    db = Database()
    created_exam=[]
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Sinav;")
        rows = cursor.fetchall()
        for row in rows:
            exam_object=Exam(row[0],row[1],row[2],row[3],row[4])
            created_exam.append(exam_object)
    return created_exam

def insertExamDataBase(exam:Exam):
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("INSERT INTO Sinav(ogretmen_id,sinav_adi,sinav_baslama_tarihi,sinav_bitis_tarihi) VALUES (%s,%s,%s,%s);",(exam.exam_ogretmen_id,exam.exam_name,exam.exam_baslama_tarihi,exam.exam_bitis_tarihi))     
    db.commit()

def insertQuestionDataBase(sinav_id,soru_icerik,soru_siklari,dogru_cevap,puan):
    #Soru(Soru_id,soru_sınav_id,soru_metni,soru_siklari,soru_dogru_cevap,soru_puani)
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("INSERT INTO Soru(soru_sinav_id,soru_metni,soru_siklari,soru_dogru_cevap,soru_puani) VALUES (%s, %s,%s,%s,%s);",(sinav_id,soru_icerik,soru_siklari,dogru_cevap,puan))
    db.commit()

#Ogrenci_Soru(ogrenci_id,soru_id,verilen_cevap,aldigi_puan)
def insertStudentQuestionDataBase(ogrenci_id,soru_id,verilen_cevap,aldigi_puan):
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("INSERT INTO Ogrenci_Soru(ogrenci_id,soru_id,verilen_cevap,aldigi_puan) VALUES (%s, %s,%s,%s);",(ogrenci_id,soru_id,verilen_cevap,aldigi_puan))
    db.commit()


def getExam(examname):
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Sinav WHERE sinav_adi= %s", (examname,))
        rows = cursor.fetchall()
        for row in rows:
            return row[0]

def getExamTotalPoint(examid):
    #Soru(Soru_id,soru_sınav_id,soru_metni,soru_siklari,soru_dogru_cevap,soru_puani)
    db=Database()
    sinav_toplam_puan=0
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Soru WHERE soru_sinav_id= %s",(examid,))
        rows=cursor.fetchall()
        for row in rows:
            sinav_toplam_puan+=int(row[5])
    return sinav_toplam_puan


def getQuestion(exam_id):
    db=Database()
    liste=[]
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Soru WHERE soru_sinav_id= %s",(exam_id,))
        rows=cursor.fetchall()
        for row in rows:
            soru_information=[row[0],row[1],row[2],row[3],row[4],row[5]]
            liste.append(soru_information) 
    return liste

def getQuestionPoint(soru_id):
    #Soru(Soru_id,soru_sınav_id,soru_metni,soru_siklari,soru_dogru_cevap,soru_puani)
    db=Database()
    liste=[]
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Soru WHERE soru_id= %s",(soru_id,))
        rows=cursor.fetchall()
        for row in rows:
            liste=[row[4],row[5]]
    return liste

def getExamId(soru_id):
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT (soru_sinav_id) FROM Soru WHERE soru_id= %s",(soru_id,))
        row=cursor.fetchone()
    return row[0]

#Ogrenci_Sinav(ogrenci_id,sinav_id,ogrenci_sinav_bitis_tarihi,dogru_sayi,yanlis_cevap,puan)
def insertStudentExamDatabase(ogrenci_id,sinav_id,sinav_bitiris_tarihi,dogru_cevap,yanlis_cevap,puan):
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("INSERT INTO Ogrenci_Sinav(ogrenci_id,sinav_id,ogrenci_sinav_bitis_tarihi,dogru_sayi,yanlis_cevap,puan) VALUES (%s, %s,%s,%s,%s,%s);",(ogrenci_id,sinav_id,sinav_bitiris_tarihi,dogru_cevap,yanlis_cevap,puan))
    db.commit()
    
def getStudentExamResult(ogrenci_id,sinav_id):
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Ogrenci_Sinav WHERE ogrenci_id= %s and sinav_id= %s",(ogrenci_id,sinav_id))
        row=cursor.fetchone()
    return [row[0],row[1],row[2],row[3],row[4],row[5]]


def getTeacherExam(ogretmen_id):
    db=Database()
    created_exam=[]
    with db.get_cursor() as cursor:
        cursor.execute("SELECT k.kullanici_adi, s.sinav_id, s.sinav_adi, s.sinav_baslama_tarihi , s.sinav_bitis_tarihi FROM Kullanici AS k JOIN Sinav As s on k.kullanici_id=s.ogretmen_id WHERE s.ogretmen_id= %s;",(ogretmen_id,))
        rows = cursor.fetchall()
        for row in rows:
            a=[row[0],row[1],row[2],row[3],row[4]]
            created_exam.append(a)
    return created_exam

def getStudentExam(ogrenci_id):
    db=Database()
    created_exam=[]
    with db.get_cursor() as cursor:
        cursor.execute("SELECT o.sinav_id,k.kullanici_adi,s.sinav_adi  FROM Kullanici AS k JOIN Ogrenci_Sinav AS o ON  k.kullanici_id = o.ogrenci_id JOIN Sinav AS s ON s.sinav_id = o.sinav_id WHERE o.ogrenci_id = %s;", (ogrenci_id,))
        rows = cursor.fetchall()
        for row in rows:
            a=[row[0],row[1],row[2]]
            created_exam.append(a)
    return created_exam


def getLeaderBoardExam(exam_id):
    db=Database()
    liste=[]
    with db.get_cursor() as cursor:
        cursor.execute("SELECT k.kullanici_adi, o.puan FROM Kullanici AS k JOIN Ogrenci_Sinav AS o ON k.kullanici_id = o.ogrenci_id WHERE o.sinav_id = %s ORDER BY o.puan DESC;",(exam_id,))
        rows=cursor.fetchall()
        for row in rows:
            a=[row[0],row[1]]
            liste.append(a)
    return liste
if args.command == "init":
    if path.exists("initialized.txt"):
        print("This project already initialized")
    else:
        try:
            create_database()
            fill_database()
            open("initialized.txt", "w+")
            print("project initialized")
        except Exception as inst:
            print("cannot initialize project: " + str(inst))

elif args.command == "destroy":
    drop_database()
    os.remove("initialized.txt")

elif args.command== "sinavtablosu":
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Sinav;")
        rows = cursor.fetchall()
        for row in rows:
            print("Öğretmen:",row[0],row[1],row[2],row[3])

elif args.command== "ogrencisorutablosu":
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Ogrenci_Soru;")
        rows = cursor.fetchall()
        for row in rows:
            print("Soru:",row[0],row[1],row[2],row[3])

elif args.command== "sorutablosu":
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Soru;")
        rows = cursor.fetchall()
        for row in rows:
            print("Soru:",row[0],row[1],row[2],row[3],row[4],row[5])


elif args.command=="ogrencisinavtablosu":
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Ogrenci_Sinav;")
        rows = cursor.fetchall()
        for row in rows:
            print("OgrenciSınav:",row[0],row[1],row[2],row[3],row[4],row[5])

elif args.command=="kullanicitablosu":
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Kullanici;")
        rows = cursor.fetchall()
        for row in rows:
            print("Kullanici:",row[0],row[1],row[2],row[3])
#Ogrenci_Sinav(ogrenci_id,sinav_id,ogrenci_sinav_bitis_tarihi,dogru_sayi,yanlis_cevap,puan)
elif args.command=="ogrenciresult":
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Ogrenci_Sinav WHERE ogrenci_id= %s and sinav_id= %s",(3,10))
        rows = cursor.fetchall()
        for row in rows:
            print("OgrenciSınavResult:",row[0],row[1],row[2],row[3],row[4],row[5])

elif args.command=="leadorboard":
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT k.kullanici_adi, o.puan FROM Kullanici AS k JOIN Ogrenci_Sinav AS o ON k.kullanici_id = o.ogrenci_id WHERE o.sinav_id = %s ORDER BY o.puan DESC;",(2,))
        rows=cursor.fetchall()
        for row in rows:
            print(row[0],row[1])

elif args.command=="ogretmengetir":
    for i in getTeacherExam(5):
        print(i)

elif args.command=="ogrencigetir":
    for i in getStudentExam(1):
        print(i)