import socket

Host = "192.168.1.27"
Port = 54950

serveur_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

serveur_client.connect((Host,Port))

while True :
    message = input('>>')
    message = message.encode('utf8')
    serveur_client.send(message)
    requete_serveur = serveur_client.recv(50)
    requete_serveur = requete_serveur.decode('utf8')
    print(requete_serveur)