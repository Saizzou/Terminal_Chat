#!/bin/python3
import socket
from threading import Thread

HOST = '' # Server IP addressini yada DynDNS giriniz!
PORT = 65432 # Server Portunu belirtiniz!
BUFFERSIZE = 1024
ADDR = (HOST, PORT)
katilimci_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
katilimci_socket.connect(ADDR)

print("Baglanti saglandi! Kendinize bir takma isim belirleyin: ")

def main():
    while True:
        data = katilimci_socket.recv(BUFFERSIZE)
        print("Gelen mesaj: ", str(data.decode('utf8')))

    katimci_socket.close()

def mesaj_yaz():
    while True:
        print("Mesaj giriniz: ")
        message = input()
        katilimci_socket.send(message.encode("utf8"))

if __name__ == '__main__':
    ACCEPT_THREAD = Thread(target=main)
    ACCEPT_THREAD2 = Thread(target=mesaj_yaz)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD2.start()
    ACCEPT_THREAD.join()
    ACCEPT_THREAD2.join()
