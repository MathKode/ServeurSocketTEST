import socket

serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

Host = "192.168.1.27"
Port = 1234

serveur.bind((Host,Port))
serveur.listen()

client, adresse = serveur.accept() 
print("le client :",adresse," s'est connecté")
while True :
    req_client = client.recv(500000).decode('utf8')
    print(req_client)
    if not req_client :
        break 
    f = open('liste.txt','a')
    f.write(req_client)
    f.close()
    print('\n____________________________________________________________________________________________________________________________\n')
client.close()
serveur.close()