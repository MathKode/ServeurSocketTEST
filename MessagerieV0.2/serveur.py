import socket
from threading import Thread

def Connecion(client,adresse):
    while True :
        requete_client = client.recv(250)
        requete_client = requete_client.decode("utf8")
        print("Client : ",requete_client)
        if not requete_client:
            print('CLOSE')
            break
        message = input('>>')
        message = message.encode("utf8")
        client.send(message)
    client.close()

Host = "192.168.1.27"
Port = 6390  

#Création du socket (serveur)
serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#Pour créer le serveur (le mettre en écoute sur un port)
serveur.bind((Host,Port))

#Nb max
serveur.listen()

liste_thread = []
#Att connexion
for i in range(5): #nombre de connection avant fermeture
    client, adresse = serveur.accept() 
    th = Thread(target=Connecion,args=(client,adresse))
    liste_thread.append(th)
    th.start()

for th in liste_thread :
    th.join()    
print('END')
client.close()
serveur.close()