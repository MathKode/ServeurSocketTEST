from threading import Thread
import socket

Host = "192.168.1.27"
Port = 1234

server_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_client.connect((Host,Port))

def Send(server_client):
    while True:
        server_client.send(input().encode('utf8'))
def Reception(server_client):
    while True:
        req = server_client.recv(5000).decode('utf8')
        print(req)

envoi = Thread(target=Send,args=[server_client])
recep = Thread(target=Reception,args=[server_client])
envoi.start()
recep.start()

envoi.join()
recep.join()