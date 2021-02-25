import socket

#créer le fichier si il n'existe pas
file = open('LoginV0.1/table.txt','a')
file.close

Host = "192.168.1.27"
Port = 6390

serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind((Host,Port))

serveur.listen(1)

client, adresse = serveur.accept()
print("Client avec l'adresse : ",adresse,"C'est connecté")

while True:
    req_client = client.recv(5000).decode('utf8')
    if not req_client:
        print('CLOSE')
        break
    print(req_client)
    if req_client == "COB":
        print('debut req')
        user_name = client.recv(5000).decode('utf8')
        file = open('LoginV0.1/table.txt','r')
        c = file.read().split('\n')
        file.close()
        contenu = []
        for i in c :
            ls = i.split('Ó')
            contenu.append(ls)
        print(contenu)
        login_name = []
        for i in contenu:
            login_name.append(i[0])
        if user_name not in login_name :
            client.send(b'USER_NAME_NOTEXIST')
        else :
            client.send(b'USER_NAME_EXIST')
            password = client.recv(5000).decode('utf8')
            right = False
            tour = 0
            for i in contenu :
                if i[0] == user_name and i[1] == password :
                    right = True
                    message = i[2]
                    i[3] = str(int(i[3]) - 1)
                    if i[3] == '0' :
                        del contenu[tour]
                tour += 1
            if right :
                file = open('LoginV0.1/table.txt','w')
                print(contenu)
                tour = 0
                for line in contenu :
                    l = "Ó".join(line)
                    print(l)
                    file.write(l)
                    if tour != len(contenu) - 1 :
                        file.write('\n')
                    tour += 1
                file.close()
                client.send(message.encode('utf8'))
            else :
                client.send(b'WRONG_PASS #03')
    if req_client == "CNL":
        new_login = client.recv(5000).decode('utf8')
        file = open('LoginV0.1/table.txt') 
        login = []
        for line in file.read().split('\n'):
            login.append(line.split('Ó')[0])
        print(login)
        if new_login not in login :
            client.send(b'LOGIN NOT EXIST')
            password = client.recv(5000).decode('utf8')
            message = client.recv(5000).decode('utf8')
            elimination = client.recv(5000).decode('utf8')
            c = [new_login,password,message,elimination]
            file = open('LoginV0.1/table.txt','a')
            file.write('\n')
            file.write("Ó".join(c))
            file.close()
            file = open('LoginV0.1/table.txt','r')
            c = file.read().split('\n')
            file.close()
            contenu = []
            for line in c :
                if line != '' :
                    contenu.append(line)
            print(contenu)
            file = open('LoginV0.1/table.txt','w')
            tour = 0
            for i in contenu :
                file.write(i)
                if tour != len(contenu) - 1 :
                    file.write('\n')
                tour += 1
            file.close()
            client.send(b'LOGIN CREATE SUCCESSFULY')
        else :
            client.send(b'LOGIN EXIT #04')
    print('FIN ACTION')



client.close()
serveur.close()
