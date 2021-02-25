import socket

#Création du socket (serveur client)
serveur_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Définition des infos sur le serveur
Host = "192.168.1.27"
Port = 6390

#On se connecte au serveur
serveur_client.connect((Host,Port))
print("Bienvenu dans MHC message hidden control,",
    "fait /help pour obtenir la liste des commandes.")
command_ls = ['/help','/log','/exit','/create']
while True :
    command = input('-> ').lower()
    if command not in command_ls :
        print('Unknown command #01')
    else :
        if command == "/help" :
            help_ls = ["Commandes : ",
                        "   /log",
                        "       Permet de se connecter à un compte",
                        "       Attention, il faut le usname et le",
                        "       password",
                        "   /create",
                        "       Permet de créer un compte",
                        "       Le symbole Ó est interdit partout!",
                        "   /exit",
                        "       Ferme la connection",
                        "INFO : les comptes vous permettes de stock",
                        "er du textes pour l'afficher lors de la pr",
                        "ochaine connexion.",
                        "Tu peux choisir ou bout de combien d'ouvert",
                        "ure sera supp la note lors de sa creation  ",
                        "                       By BiMathAx STUDIO"]
            for i in help_ls : print(i)
        if command == "/log":
            serveur_client.send(b"COB")
            login = input("User Name : ").encode('utf8')
            serveur_client.send(login)
            req_serv = serveur_client.recv(21).decode('utf8')
            if req_serv == "USER_NAME_EXIST" :
                password = input('Password : ').encode('utf8')
                serveur_client.send(password)
                message = serveur_client.recv(5000).decode('utf8')
                print(message)
                
            else :
                print("USER NAME NOT EXIST #02")
        if command == '/exit':
            print("CLOSE")
            break
        if command == "/create" :
            serveur_client.send(b'CNL')
            login = input('New user name : ').encode('utf8')
            serveur_client.send(login)
            reponse_serveur = serveur_client.recv(50).decode('utf8')
            if reponse_serveur == "LOGIN NOT EXIST" :
                serveur_client.send(input('Password : ').encode('utf8'))
                serveur_client.send(input('Message : ').encode('utf8'))
                serveur_client.send(input('Number of see before elimination : ').encode('utf8'))
                reponse = serveur_client.recv(50).decode('utf8')
                print(reponse)
            else :
                print(reponse_serveur)
    