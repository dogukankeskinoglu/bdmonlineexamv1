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
#Kullanıcı(kullanici_id,kullanici_adi,sifre,kullanici_type)
#Sınav(sınav_id,ogretmen_id,sinav_adi,sınav_baslama,sınav_bitis)
#Ogrenci_Sınav(ogrenci_id,sinav_id,ogrenci_dogru_sayı,ogrenci_yanlis_sayı,ogrenci_puan)
#Soru(Soru_id,soru_sınav_id,soru_metni,soru_siklari,soru_dogru_cevap,soru_puani)
#Ogrenci_Soru(ogrenci_id,soru_id,verilen_cevap,aldigi_puan)

def create_database():
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("CREATE TABLE Kullanici (kullanici_id serial PRIMARY KEY,kullanici_adi VARCHAR(50) NOT NULL,kullanici_sifre VARCHAR(50) NOT NULL,kullanici_tipi VARCHAR(50) NOT NULL);")
        cursor.execute("CREATE TABLE Sinav(sinav_id serial PRIMARY KEY,sinav_adi VARCHAR(50) NOT NULL,sinav_baslama_tarihi timestamp  NOT NULL,sinav_bitis_tarihi timestamp NOT NULL);")
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
            exam_object=Exam(row[0],row[1],row[2],row[3])
            created_exam.append(exam_object)
    return created_exam

def insertExamDataBase(exam:Exam):
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("INSERT INTO Sinav(sinav_adi,sinav_baslama_tarihi,sinav_bitis_tarihi) VALUES (%s, %s,%s);",(exam.exam_name,exam.exam_baslama_tarihi,exam.exam_bitis_tarihi))     
    db.commit()

def insertQuestionDataBase(sinav_id,soru_icerik,soru_ciklari,dogru_cevap,puan):
    #Soru(Soru_id,soru_sınav_id,soru_metni,soru_siklari,soru_dogru_cevap,soru_puani)
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("INSERT INTO Soru(soru_sinav_id,soru_metni,soru_siklari,soru_dogru_cevap,soru_puani) VALUES (%s, %s,%s,%s,%s);",(sinav_id,soru_icerik,soru_ciklari,dogru_cevap,puan))
    db.commit()

def getExam(examname):
    db=Database()
    with db.get_cursor() as cursor:
        cursor.execute("SELECT * FROM Sinav WHERE sinav_adi= %s", (examname,))
        rows = cursor.fetchall()
        for row in rows:
            return row[0]
  


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
