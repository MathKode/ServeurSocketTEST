from threading import Thread
import socket

host = "192.168.1.24"
port = 10500

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen(5)

global client_ls
client_ls = []

def send(msg,client_sender):
    #client_ls_without_the_client_who_send_message
    ls = []
    for client in client_ls:
        if client != client_sender:
            ls.append(client)
    for client in ls:
        try:
            client.send(str(msg).encode())
        except:
            #Case of deconnection
            pass

def recep(client):
    while True:
        try:
            msg = client.recv(1024).decode()
            send(msg,client)
        except:
            break
    client_ls.remove(client)
    send(f"--- ONE LEFT ---\n{len(client_ls)} still connected",client)
    client.close()
    
thread_ls = []
while True:
    client, ip = server.accept()
    print("CONNETION",ip[0])
    client_ls.append(client)
    thread_ls.append(Thread(target=recep,args=[client]))
    thread_ls[-1].start()
    send(f"--- NEW CLIENT ---\n{len(client_ls)} are connected", "server")
    
