import argparse
import os
from os import path
from database import Database

parser = argparse.ArgumentParser(description='App manager.')
parser.add_argument('command', metavar="cmd", type=str, help='command to manage the app')

args = parser.parse_args()

#Kullanıcı(kullanici_id,kullanici_adi,sifre,kullanici_type)
#Sınav(sınav_id,ogretmen_id,sinav_adi,sınav_baslama,sınav_bitis)
#Ogrenci_Sınav(ogrenci_id,sinav_id,ogrenci_dogru_sayı,ogrenci_yanlis_sayı,ogrenci_puan)
#Soru(Soru_id,soru_sınav_id,soru_metni,soru_siklari,soru_dogru_cevap,soru_puanı)
#Ogrenci_Soru(ogrenci_id,soru_id,verilen_cevap,aldigi_puan)
"""
CREATE TABLE contacts(
   contact_id INT GENERATED ALWAYS AS IDENTITY,
   customer_id INT,
   contact_name VARCHAR(255) NOT NULL,
   phone VARCHAR(15),
   email VARCHAR(100),
   PRIMARY KEY(contact_id),
   CONSTRAINT fk_customer
      FOREIGN KEY(customer_id) 
      REFERENCES customers(customer_id)
);
"""
def create_database():
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("CREATE TABLE Kullanici (kullanici_id serial PRIMARY KEY,kullanici_adi VARCHAR(50) NOT NULL,kullanici_sifre VARCHAR(50) NOT NULL,kullanici_tipi VARCHAR(50) NOT NULL);")
        cursor.execute("CREATE TABLE Sınav(sinav_id serial PRIMARY KEY,ogretmen_id INTEGER NOT NULL,sinav_adi VARCHAR(50) NOT NULL,sinav_baslama_zamani DATETIME NOT NULL,sinav_bitis_tarihi DATETIME NOT NULL,FOREIGN KEY (ogretmen_id) REFERENCES Kullanici(kullanici_id));")
        cursor.execute("CREATE TABLE Soru(soru_id serial PRIMARY KEY,soru_sinav_id INTEGER NOT NULL,soru_metni VARCHAR(MAX) NOT NULL,soru_siklari VARCHAR(MAX) NOT NULL,soru_dogru_cevap CHAR(1) NOT NULL,soru_puanı INTEGER NOT NULL,FOREIGN KEY(soru_sinav_id) REFERENCES Sınav(sinav_id));")
        cursor.execute("CREATE TABLE Ogrenci_Soru(ogrenci_id INTEGER,soru_id INTEGER ,verilen_cevap CHAR(1) NOT NULL,aldigi_puan INTEGER NOT NULL,PRIMARY KEY(ogrenci_id,soru_id),FOREIGN KEY(ogrenci_id) REFERENCES Kullanici(kullanici_id),FOREIGN KEY (soru_id) REFERENCES Soru(soru_id));")
        cursor.execute("CREATE TABLE Ogrenci_Sınav(ogrenci_id INTEGER,sinav_id INTEGER,ogrenci_sinav_bitişi DATETIME NOT NULL,dogru_sayi INTEGER NOT NULL ,yanlis_cevap INTEGER NOT NULL ,puan INTEGER NOT NULL,PRIMARY KEY(ogrenci_id,sinav_id),FOREIGN KEY(ogrenci_id) REFERENCES Kullanici(kullanici_id),FOREIGN KEY(sinav_id) REFERENCES Sınav(sinav_id));")
    db.commit()
    print("Finished creating table")




def drop_database():
    db = Database()
    with db.get_cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS Kullanici;")
        cursor.execute("DROP TABLE IF EXISTS Sınav;")
        cursor.execute("DROP TABLE IF EXISTS Soru;")
        cursor.execute("DROP TABLE IF EXISTS Ogrenci_Soru;")
        cursor.execute("DROP TABLE IF EXISTS Ogrenci_Sınav;")
    db.commit()
    print("Finished dropping tables")


if args.command == "init":
    if path.exists("initialized.txt"):
        print("This project already initialized")
    else:
        try:
            create_database()
            #fill_database()
            open("initialized.txt", "w+")
            print("project initialized")
        except Exception as inst:
            print("cannot initialize project: " + str(inst))

elif args.command == "destroy":
    drop_database()
    os.remove("initialized.txt")
