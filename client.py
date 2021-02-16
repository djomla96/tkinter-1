import tkinter as tk
from tkinter import *
from tkinter import messagebox
import socket
from threading import Thread
import time

port = 80

root = tk.Tk()
root.geometry('800x800')
root.config(bg="silver")
root.title("KLIJENT")
header = tk.Frame(root, bg='gray', height=50)
content = tk.Frame(root, bg='silver',height=700)
footer = tk.Frame(root, bg='gray', height=50)

####################################################  header
# files = ["C:\\Users\\Mili\\Desktop\\Animacija\\Slika1.png", "C:\\Users\\Mili\\Desktop\\Animacija\\Slika2.png","C:\\Users\\Mili\\Desktop\\Animacija\\Slika3.png","C:\\Users\\Mili\\Desktop\\Animacija\\Slika4.png","C:\\Users\\Mili\\Desktop\\Animacija\\Slika5.png","C:\\Users\\Mili\\Desktop\\Animacija\\Slika6.png","C:\\Users\\Mili\\Desktop\\Animacija\\Slika7.png"]
# photos = [PhotoImage(file=x) for x in files]
# label = Label(header)
# label.photos = photos
# label.counter = 0
# class animacija(Thread):
#     def __init__(self):
#         Thread.__init__(self)
#         self.daemon = True
#         self.start()
#     def run(self):
#         while True:
#             label['image'] = label.photos[label.counter%len(label.photos)]
#             label.counter += 1
#             time.sleep(0.1)
#             label.pack()
# t = Thread (target=animacija)
# t.start()

############################################################content

############################################################ funckija za dugme kreirajTabelu
def kreirajPraznuTabelu():
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, port))
    message="Kreiraj novu bazu."
    s.send(message.encode())
    odgovor = s.recv(1024).decode()
    odgovoriServera.insert("end", odgovor)
    s.close()
kreirajTabelu = Button(content, text ="Kreiraj praznu tabelu", relief=RAISED,bg="grey",fg="white",command=kreirajPraznuTabelu, font=("Cilibric", "12"))
kreirajTabelu.pack(pady=20)
############################################################
frameUnos=Frame(content,bg="silver")
frameUnos.pack()


idUnosLbl=Label(frameUnos,text="ID:",fg="gray",bg="silver", font=("Cilibric", "16"))
idUnosLbl.pack(side=LEFT)
idUnos=Entry(frameUnos ,bg="white",fg="gray",width=20)
idUnos.pack(side=LEFT)

imeUnosLbl=Label(frameUnos,text="Naziv:",fg="gray",bg="silver", font=("Cilibric", "16"))
imeUnosLbl.pack(side=LEFT)
imeUnos=Entry(frameUnos ,bg="white",fg="black",width=20)
imeUnos.pack(side=LEFT)

cenaUnosLbl=Label(frameUnos,text="Cena:",fg="gray",bg="silver", font=("Cilibric", "16"))
cenaUnosLbl.pack(side=LEFT)
cenaUnos=Entry(frameUnos ,bg="white",fg="black",width=20)
cenaUnos.pack(side=LEFT)
def unesiUTabelu():
    try:
        int(idUnos.get())
        float(cenaUnos.get())
    except:
        messagebox.showerror("Error", "Nije validan unos!")
        return
    if not (idUnos.get() and imeUnos.get() and cenaUnos.get()):
        messagebox.showerror("Error", "Nije validan unos!")
        return
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, port))
    message="Unesi podatke u bazu:%s,%s,%s" % (idUnos.get(), imeUnos.get(),cenaUnos.get())
    s.send(message.encode())
    odgovor = s.recv(1024).decode()
    odgovoriServera.insert("end", odgovor)
    s.close()
    idUnos.delete(0, END)
    imeUnos.delete(0, END)
    cenaUnos.delete(0, END)
unesi = Button(frameUnos, text ="Unesi podatke u tabelu", relief=RAISED, bg="gray", fg="white",command=unesiUTabelu, font=("Cilibric", "12"))
unesi.pack( padx=30)

framePretraga=Frame(content,bg="silver")
framePretraga.pack(padx=20, pady=20)

idPretragaLbl=Label(framePretraga,text="ID:",fg="grey",bg="silver", font=("Cilibric", "16"))
idPretragaLbl.pack(side=LEFT)
def pretraziPoId():
    try:
        int(idPretraga.get())
    except:
        messagebox.showerror("Error", "Nije validan unos!")
        return
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, port))
    message = "Pretrazi po id-u:%s" % (idPretraga.get())
    s.send(message.encode())
    odgovor = s.recv(1024).decode()
    odgovoriServera.insert("end", odgovor)
    if ":" in odgovor:
        naziv, cena = odgovor.split(":")[1].split(",")
        cena = float(cena)
        ispis = "Naziv: " + naziv + " Cena: " + str(cena)
        ispisPodataka.configure(state="normal")
        ispisPodataka.delete(0, tk.END)
        ispisPodataka.insert(0, ispis)
        ispisPodataka.configure(state="disabled")
    s.close()
    idPretraga.delete(0, END)

idPretraga=Entry(framePretraga ,bg="white",fg="grey",width=20)
idPretraga.pack(side=LEFT)
pretraziId = Button(framePretraga, text ="Pretrazi po ID-u", relief=RAISED, bg="grey", fg="white",command=pretraziPoId, font=("Cilibric", "12"))
pretraziId.pack(side=LEFT,padx=20)

def pretraziPoCeni():
    try:
        float(cenaPretraga.get())
    except:
        messagebox.showerror("Error", "Nije validan unos!")
        return
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, port))
    message = "Pretrazi po ceni:%s" % (cenaPretraga.get())
    s.send(message.encode())
    odgovor = s.recv(1024).decode()
    odgovoriServera.insert("end", odgovor)
    if ":" in odgovor:
        id, naziv = odgovor.split(":")[1].split(",")
        id = int(id)
        ispis = "Id: " + str(id) + " Naziv: " + str(naziv)
        ispisPodataka.configure(state="normal")
        ispisPodataka.delete(0, tk.END)
        ispisPodataka.insert(0, ispis)
        ispisPodataka.configure(state="disabled")
    s.close()
    cenaPretraga.delete(0, END)
cenaPretragaLbl=Label(framePretraga,text="Cena:",fg="grey",bg="silver", font=("Cilibric", "16"))
cenaPretragaLbl.pack(side=LEFT)
cenaPretraga=Entry(framePretraga ,bg="white",fg="grey",width=20)
cenaPretraga.pack(side=LEFT)
pretraziCenu = Button(framePretraga, text ="Pretrazi po ceni", relief=RAISED, bg="grey", fg="white",command=pretraziPoCeni, font=("Cilibric", "12"))
pretraziCenu.pack( side=LEFT,padx=20)

frameIspis=Frame(content,bg="silver")
frameIspis.pack(padx=20, pady=20)
ispisPodatakaLbl=Label(frameIspis,text="Informacije o automobilu:",fg="grey",bg="silver", font=("Cilibric", "16"))
ispisPodatakaLbl.pack(side=LEFT)
ispisPodataka=Entry(frameIspis ,bg="white",fg="grey",width=60,state='disabled')
ispisPodataka.pack(side=LEFT)

frameAzuriranje=Frame(content,bg="silver")
frameAzuriranje.pack(padx=20, pady=20)
def promenaCene():
    try:
        int(idAzuriranje.get())
        float(cenaAzuriranje.get())
    except:
        messagebox.showerror("Error", "Nije validan unos!")
        return
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, port))
    message = "Azuriraj cenu za dati id:%s,%s" % (idAzuriranje.get(),cenaAzuriranje.get())
    s.send(message.encode())
    odgovor = s.recv(1024).decode()
    odgovoriServera.insert("end", odgovor)
    s.close()
    idAzuriranje.delete(0, END)
    cenaAzuriranje.delete(0, END)
idAzuriranjeLbl=Label(frameAzuriranje,text="ID automobila:",fg="grey",bg="silver", font=("Cilibric", "16"))
idAzuriranjeLbl.pack(side=LEFT)
idAzuriranje=Entry(frameAzuriranje ,bg="white",fg="grey",width=20)
idAzuriranje.pack(side=LEFT)

cenaAzuriranjeLbl=Label(frameAzuriranje,text="Nova cena automobila:",fg="grey",bg="silver", font=("Cilibric", "16"))
cenaAzuriranjeLbl.pack(side=LEFT)
cenaAzuriranje=Entry(frameAzuriranje ,bg="white",fg="grey",width=20)
cenaAzuriranje.pack(side=LEFT)
azuriraj = Button(frameAzuriranje, text ="Azuriraj", relief=RAISED, bg="grey", fg="white",command=promenaCene, font=("Cilibric", "12"))
azuriraj.pack( side=LEFT,padx=20)

frameBrisanje=Frame(content,bg="silver")
frameBrisanje.pack(padx=20, pady=20)
def brisanje():
    if not nazivBrisanje.get():
        messagebox.showerror("Error", "Nije validan unos!")
        return
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, port))
    message = "Obrisi za dati naziv:%s" % (nazivBrisanje.get())
    s.send(message.encode())
    odgovor = s.recv(1024).decode()
    odgovoriServera.insert("end", odgovor)
    s.close()
    nazivBrisanje.delete(0, END)
nazivBrisanjeLbl=Label(frameBrisanje,text="Naziv automobila za brisanje:",fg="grey",bg="silver", font=("Cilibric", "16"))
nazivBrisanjeLbl.pack(side=LEFT)
nazivBrisanje=Entry(frameBrisanje ,bg="white",fg="grey",width=20)
nazivBrisanje.pack(side=LEFT)
obrisi = Button(frameBrisanje, text ="Obrisi", relief=RAISED, bg="grey", fg="white",command=brisanje, font=("Cilibric", "12"))
obrisi.pack( side=LEFT,padx=20)

odgovoriSeveraLbl=Label(content,text="Odgovori servera:",fg="grey",bg="silver")
odgovoriSeveraLbl.pack()
odgovoriServera=Listbox(content,bg="silver",fg="grey",width=70)
odgovoriServera.pack()
###########################################################konekcija
#s = socket.socket()
#host = socket.gethostname()
#port = 80
#s.connect((host, port))
#print (s.recv(1024).decode())
#s.close()
#############################################################footer
name = tk.Label(footer,bg='gray',fg='white', text="© 2020. Mladjan Milosavljevic RIN-49/19")
name.config(font=("Cilibric", "16"))
name.pack()

header.pack(fill='both')
content.pack(fill='both')
footer.pack(fill='both', side='bottom')
root.mainloop()