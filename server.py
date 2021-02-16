import tkinter as tk
import sqlite3
import socket
from re import search
from threading import Thread
from tkinter import *

root = tk.Tk()
root.geometry('250x800')
root.config(bg="orange")
odgovoriSeveraLbl=Label(root,text="SERVER",fg="Black",bg="orange", font=('bold'))
odgovoriSeveraLbl.pack()
odgovoriServera=Listbox(root,bg="orange",fg="dark blue",width=70,height=700)
odgovoriServera.pack()
##########################################konekcija
def startConnection():
    cenaAna = 0
    cenaEna = 0
    s = socket.socket()
    host = socket.gethostname()
    port = 80
    s.bind((host, port))
    s.listen(5)

    while True:

        conn, addr = s.accept()
        print ('Konekcija sa', addr)
        odgovoriServera.insert("end", "Konekcija sa"+str(addr))

        message = conn.recv(1024).decode()
        if(message=="Kreiraj novu bazu."):
            baza = sqlite3.connect('baza01.db')  # ako je ":memory:" onda je sve u RAMu
            try:
                baza.execute('''CREATE TABLE AUTOMOBILI
                (ID INT PRIMARY KEY NOT NULL,
                NAZIV TEXT NOT NULL,
                CENA DOUBLE NOT NULL);''')
                odg="Tabela uspesno kreirana!"
            except:
                odg="Tabela vec postoji!"
            finally:
                baza.close()
                conn.send(odg.encode())
                conn.close()
        elif (search("Unesi podatke",message)):
            id, naziv, cena = message.split(":")[1].split(",")
            id = int(id)
            cena = float(cena)
            try:
                baza = sqlite3.connect('baza01.db')
                sql = """INSERT INTO AUTOMOBILI(ID, NAZIV, CENA) VALUES (?,?,?)"""
                cursor = baza.cursor()
                cursor.execute(sql, (id,naziv,cena))
                baza.commit()
                odg = "Podaci za automobil uneti!"
                baza.close()
            except Exception as e:
                odg = "Greska pri unosu!"
                print(e)
            conn.send(odg.encode())
            conn.close()
        elif (search("Doniraj:",message)):

            imeDonora, donacija = message.split(":")[1].split(",")
            if(search("ana", imeDonora)):
                cenaAna=cenaAna+int(donacija)
                odg="Ana:%s"% (str(cenaAna))

            elif((search("ena", imeDonora))):
                cenaEna=cenaEna+int(donacija)
                odg = "Ena:%s" % (str(cenaEna))

            conn.send(odg.encode())
        elif (search("Pretrazi po id-u",message)):
            id = int(message.split(":")[1])
            try:
                baza = sqlite3.connect('baza01.db')
                sql = """ SELECT * FROM AUTOMOBILI WHERE ID=? """
                cursor = baza.cursor()
                cursor.execute(sql, (id,))
                podaci_torka = cursor.fetchone()
                id,naziv,cena=podaci_torka
                odg = "Podaci za automobil:"+naziv+","+str(cena)
                baza.commit()
                print(id)
                print(odg)
                baza.close()
            except Exception as e:
                print(e)
                odg = "Greska"
            conn.send(odg.encode())
            conn.close()
        elif (search("Pretrazi po ceni",message)):
            cena = float(message.split(":")[1])
            try:
                baza = sqlite3.connect('baza01.db')
                sql = """ SELECT * FROM AUTOMOBILI WHERE CENA=? """
                cursor = baza.cursor()
                cursor.execute(sql, (cena,))
                podaci_torka = cursor.fetchone()
                id,naziv,cena=podaci_torka
                odg = "Podaci za automobil:"+str(id)+","+str(naziv)
                baza.commit()
                print(id)
                print(odg)
                baza.close()
            except Exception as e:
                print(e)
                odg = "Greska"
            conn.send(odg.encode())
            conn.close()
        elif (search("Azuriraj cenu za dati id", message)):
            id, cena = message.split(":")[1].split(",")
            id = int(id)
            cena = float(cena)
            try:
                baza = sqlite3.connect('baza01.db')
                sql = """ UPDATE AUTOMOBILI SET CENA=? WHERE ID=?"""
                cursor = baza.cursor()
                cursor.execute(sql, (cena,id))
                baza.commit()
                odg = "Cena azurirana!"
                baza.close()
            except Exception as e:
                odg = "Greska prilikom azuriranja!"
                print(e)
            conn.send(odg.encode())
            conn.close()
        elif (search("Obrisi za dati naziv", message)):
            naziv = message.split(":")[1]
            try:
                baza = sqlite3.connect('baza01.db')
                sql = """ DELETE FROM AUTOMOBILI WHERE NAZIV=?"""
                cursor = baza.cursor()
                cursor.execute(sql, (naziv,))
                baza.commit()
                odg = "Automobil uklonjen iz tabele!"
                baza.close()
            except Exception as e:
                odg = "Greska prilikom brisanja!"
                print(e)
            conn.send(odg.encode())
            conn.close()
        odgovoriServera.insert("end", message)
        odgovoriServera.insert("end", odg)

t = Thread (target=startConnection)
t.start()
####################################


root.mainloop()