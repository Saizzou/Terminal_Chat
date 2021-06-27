#!/bin/python3
import socket
from threading import Thread


katilimcilar = {}
adressler = {}

HOST = '' # Host icin IP veya DynDNS giriniz
PORT = 65432 # Burda Port degistirmek isteyebilirsiniz!
BUFFERSIZE = 1024 # Paket büyüklügü
ADDR = (HOST,PORT)
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind(ADDR)

def gelen_kontrol():
    while True:
        katilimci, katilimci_adress = SERVER.accept()
        print(f"{katilimci_adress} baglandi!")
        katilimci.send(bytes("Baglanti saglandi!", "utf8"))
        adressler[katilimci] = katilimci_adress
        Thread(target=katilimci_baglantisi, args=(katilimci,)).start()


def katilimci_baglantisi(katilimci):
    isim = katilimci.recv(BUFFERSIZE).decode("utf8")
    msg = "%s baglanti sagladi" %isim
    broadcast(bytes(msg, "utf8"))
    katilimcilar[katilimci] = isim
    while True:
        msg = katilimci.recv(BUFFERSIZE)
        if msg != bytes("{cikis}", "utf8"):
            broadcast(msg, isim+": ")
            print(isim, ": ", msg)
        else:
            katilimci.send(bytes("{cikis}", "utf8"))
            katilimci.close()
            del katilimcilar[katilimci]
            broadcast(bytes("%s cikis yapti" %isim, "utf8"))
            break


def broadcast(msg, prefix=""):
    for sock in katilimcilar:
        sock.send(bytes(prefix, "utf8")+msg)

while True:
    SERVER.listen()
    print("Baglanti bekleniyor...")
    ACCEPT_THREAD = Thread(target=gelen_kontrol)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
