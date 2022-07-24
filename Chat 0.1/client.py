from threading import Thread
import socket

host = "192.168.1.24"
port = 10500

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))

def send(client):
    while True:
        msg=input("").encode()
        client.send(msg)

def reception(client):
    while True:
        msg=client.recv(1024).decode()
        print(msg)
    
send_process = Thread(target=send,args=[client])
recep_process = Thread(target=reception,args=[client])

send_process.start()
recep_process.start()

send_process.join()
recep_process.join()

client.close()