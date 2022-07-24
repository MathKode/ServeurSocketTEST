import argparse

parser = argparse.ArgumentParser(description='This code has been created to send a file between two PC on the local net')

parser.add_argument('-r','--role',metavar="[S]erver or [C]lient",type=str,help='The role of the machine where the code is running')
parser.add_argument('-i','--server',metavar='IP',default="192.168.1.1",type=str,help="The IP of the server machine")
parser.add_argument('-f','--file',metavar='name',default=None,type=str,help="The name of the file (only if the role is client)")
parser.add_argument('-p','--port',type=int,default=5746,help="The Port of the server (optionnal)")
parser.add_argument('-b','--byte',type=int,default=8500,help="The number of byte send in one request (max 130020 but with bug, so we advice a max at 10000)")
parser.add_argument('-t','--time',type=int,default=0.2,help="Time to sleep between 2 sending of data")

args = parser.parse_args()

def progress_bar(long,c1,c2,nb):
    oc_case = int(nb*long/100)
    return str(c1*oc_case + c2*(long-oc_case))

def server(args):
    import binascii
    import socket
    import time
    import os

    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.bind((args.server,args.port))
    socket.listen(1)

    client, addr = socket.accept()
    print("Connection set up with :",addr)

    #Reception de la variable byte
    byte = ""
    while True: # Ex : 234 -> 2 puis 3 puis 4 puis S (pour signifier l'arrêt du code)
        reception = client.recv(1).decode('utf-8')
        if not reception or reception == 'S':
            break
        else :
            byte += reception
    print("The variable byte is :",byte)

    #Reception de la taille du fichier chiffre après chiffre
    size = ""
    while True: # Ex : 234 -> 2 puis 3 puis 4 puis S (pour signifier l'arrêt du code)
        reception = client.recv(1).decode('utf-8')
        if not reception or reception == 'S':
            break
        else :
            size += reception
    print("The size of the file is :",size)

    number_send = int(size)/int(byte)
    if str(number_send).split('.')[-1][0] != "0":
        number_send = int(str(number_send).split('.')[0]) + 1
    else :
        number_send = int(str(number_send).split('.')[0])
    print("Le fichier sera reçu en :",number_send,"étape(s)")

    file = []
    er = []
    for i in range(number_send):
        reception = client.recv(int(byte)).decode('utf-8') # 131020 is the max of letter (with the encodage...) because 1048576 bytes is the max of bytes
        print('Transfert :',int(i*100/(int(number_send)-1)),"% ",progress_bar(14,"■","□",int(i*100/int(number_send))),end='\r')
        if not reception :
            print('ERROR : The client has bugged')
            client.close()
            socket.close()
            exit(0)
        else :
            file.append(reception)
        #Gestion ERREUR
        if len(reception) != int(byte) and i != number_send-1:
            #print("PERTE DATA at ligne :",i,"AVEC UNE RECEPTION DE :",len(reception),len(reception) != byte)
            er.append(i)
        time.sleep(args.time)
    print("Transfert END                             ")
    

    client.send("F".encode('utf-8'))
    #Marqueur (attente de la fin de l'autre code)
    while True :
        reception = client.recv(1).decode('utf-8')
        if reception == "F":
            break


    print("Récupération des données (erreus)")
    
    print(er)

    #Récupération des lignes mals envoyés (erreurs)
    for i in er:
        print(i)
        find = True
        while find :
            for j in str(i):
                client.send(str(j).encode("utf-8"))
            client.send("S".encode("utf-8"))
            reception = client.recv(int(byte)).decode('utf-8')
            if len(reception) == int(byte):
                file[int(i)] = reception
                find = False
                #print("Erreur Save :",i)
    print('Envoi S')
    client.send("S".encode('utf-8'))

    client.send("F".encode('utf-8'))
    #Marqueur (attente de la fin de l'autre code)
    while True :
        reception = client.recv(1).decode('utf-8')
        if reception == "F":
            break

    fil = open('file.txt','w')
    fil.write("\n".join(file))
    fil.close()
    #Récupération du nom
    name = ""
    while True: 
        reception = client.recv(1).decode('utf-8')
        if not reception :
            break
        else :
            name += reception
    
    print("The name of the file is :",name)
    
    if name in os.listdir():
        print("File nammed like this exist to the reception")
        print("Rename :",name,"->",str("VR2_" +name))
        name = str("VR2_" +name)
    else :
        print('This name file doesn t exist')
    hexa = binascii.unhexlify("".join(file))
    file = open(name,'wb')
    file.write(hexa)
    file.close()

    client.close()
    socket.close()
        

def client(args):
    import binascii
    import socket
    import time
    import random
    import os
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.connect((args.server,args.port))
    file = open(str(args.file),'rb')
    content = file.read()
    file.close()
    hexa = str(binascii.hexlify(content))[2:-1]
    byte = str(args.byte) + "S"
    for i in byte :
        socket.send(i.encode('utf8'))
    print('File size :',len(hexa))
    size = str(len(hexa)) + "S"
    for i in size :
        socket.send(i.encode('utf8'))
    size = size[:-1]

    number_send = int(size)/int(args.byte)
    if str(number_send).split('.')[-1][0] != "0":
        number_send = int(str(number_send).split('.')[0]) + 1
    else :
        number_send = int(str(number_send).split('.')[0])
    print("Le fichier sera envoyé en :",number_send,"étape")

    hexa2 = []
    for i in range(number_send):
        print('Transfert :',int(i*100/(int(number_send)-1)),"% ",progress_bar(14,"■","□",int(i*100/int(number_send))),end='\r')
        if len(hexa) > int(args.byte) :
            data = hexa[:int(args.byte)]
            hexa = hexa[int(args.byte):]
        else :
            data = hexa
            print("DERNIER")
        hexa2.append(data)
        socket.send(data.encode('utf8'))
        time.sleep(args.time)
    
    
    while True :
        reception = socket.recv(1).decode('utf-8')
        if reception == "F":
            break
    socket.send("F".encode('utf-8'))


    file = open('hexa2.txt','w')
    file.write("\n".join(hexa2))
    file.close()
    #Err
    while True:
        ligne = ""
        s1 = True
        while s1: # Ex : 234 -> 2 puis 3 puis 4 puis S (pour signifier l'arrêt du code)
            reception = socket.recv(1).decode('utf-8')
            if not reception or reception == 'S':
                s1 = False
            else :
                ligne += reception
        if ligne == "":
            break
        b = int(ligne)
        print(b)
        socket.send(str(hexa2[b]).encode('utf-8'))
    
    while True :
        reception = socket.recv(1).decode('utf-8')
        if reception == "F":
            break
    socket.send("F".encode('utf-8'))

    #Name
    print('Name is :',str(args.file))
    for i in str(args.file):
        socket.send(i.encode('utf8'))
    print('Transfert END')

def main(args):
    if str(args.role).lower() == "s":
        server(args)
    else :
        client(args)

if __name__ == "__main__":
    main(args)