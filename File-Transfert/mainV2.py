import argparse

parser = argparse.ArgumentParser(description='This code has been created to send a file between two PC on the local net')

parser.add_argument('-r','--role',metavar="[S]erver or [C]lient",type=str,help='The role of the machine where the code is running. Client is the machine who send the file and server the one who receive the file')
parser.add_argument('-i','--ip',metavar='SERVER IP',default="192.168.1.1",type=str,help="The IP of the server machine")
parser.add_argument('-f','--file',metavar='name',default=None,type=str,help="The name of the file (only if the role is client)")
parser.add_argument('-p','--port',type=int,default=5746,help="The Port of the server (optionnal)")
parser.add_argument('-b','--byte',type=int,default=8500,help="The number of byte send in one request (max 130020 but with bug, so we advice a max at 10000)")

args = parser.parse_args()

def progress_bar(long,c1,c2,nb):
    oc_case = int(nb*long/100)
    return str(c1*oc_case + c2*(long-oc_case))

def server(args):
    import socket
    import binascii
    import os
    print("--- Creating of server ---")
    
    if os.name == "nt" :
        #Windows
        ip = args.ip
    else :
        #MacOs
        terminal = os.popen("ifconfig")
        ip = terminal.read().split("broadcast")[0]
        ip = str(ip[-60:].split('inet ')[1]).split(" ")[0]
    
    print('Your IP :',ip)
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.bind((ip,args.port))
    socket.listen(1)
    print("Waiting of a connection...",end='\r')
    client, ip = socket.accept()
    print("Connection with the client ip :",ip)

    #Reception du nom du fichier
    print("Reception of the name...",end='\r')
    len_ = ""
    while True:
        rep = client.recv(1).decode('utf-8')
        if not rep :
            print("Le client s'est déco")
            client.close()
            socket.close()
        if rep == "S" :
            break
        else :
            len_ += rep
    name_file = ""
    for i in range(int(len_)):
        rep = client.recv(1).decode('utf-8')
        name_file += rep
    print("The Name of the file :",name_file)

    #Reception du nombre d'envoie
    print("Reception send number...",end='\r')
    send_nb = ""
    while True:
        rep = client.recv(1).decode('utf-8')
        if not rep :
            print("Le client s'est déco")
            client.close()
            socket.close()
        if rep == "S" :
            break
        else :
            send_nb += rep
    send_nb = int(send_nb)
    print("The number of send is :",send_nb)

    #Reception de la variable byte
    print("Reception byte...",end='\r')
    byte = ""
    while True:
        rep = client.recv(1).decode('utf-8')
        if not rep :
            print("Le client s'est déco")
            client.close()
            socket.close()
        if rep == "S" :
            break
        else :
            byte += rep
    byte = int(byte)
    print("Byte is defined on :",byte)

    #Reception de la variable last_line_len
    print("Reception l_l_l vr...",end='\r')
    last_line_len = ""
    while True:
        rep = client.recv(1).decode('utf-8')
        if not rep :
            print("Le client s'est déco")
            client.close()
            socket.close()
        if rep == "S" :
            break
        else :
            last_line_len += rep
    last_line_len = int(last_line_len)
    print("Last line len is defined on :",last_line_len)

    #Reception fichier
    hexa_list = []
    t = 0
    while True:
        rep = client.recv(byte).decode('utf-8')
        #if len(rep) not in [last_line_len,byte,1,2]:
            #print("ERREUR ",t)
        if not rep :
            print("Le client s'est déco")
            client.close()
            socket.close()
        if last_line_len == 1 and rep == "SS" :
            break
        elif last_line_len != 1 and rep == "S" :
            break
        else :
            hexa_list.append(rep)
        print('Transfert :',int(t*100/(int(send_nb)-1)),"% ",progress_bar(14,"■","□",int(t*100/int(send_nb-1))),end='\r')
        t += 1
    
    hexa = binascii.unhexlify("".join(hexa_list))
    file = open(name_file,'wb')
    file.write(hexa)
    file.close()
    
    print("--- END ---                           ")

    client.close()
    socket.close()

def client(args):
    """
    // Syntax
    -> = socket.send
    <- = socket.recv
    ~> = exemple de ce que a quoi ça va servir (pas d'envoi tout de suite)

    // La méthode utilisé pour envoyer le nom du fichier est la suivante :
    fichier1.png = longueur de 12 caractères
        -> 1
        -> 2
        -> S
    La S signifie STOP
    ~puis on envoie :
        -> f
        -> i
        ...
        -> 1
        -> .
        -> p
        -> n
        -> j
    
    // Verif que vr byte < nb caractères hexa
    Car si (exemple) byte = 8500 et que len(hexa) = 400 : Ca bug
    On modifie donc byte pour que byte = 399 (byte > len(hexa))

    // La méthode de calcul du nombre d'envoie est très simple. Elle conciste a
    calculer le nombre de SEND que l'on va devoir faire pour transmettre le fichier
    20 000 caractères hexadécimals et --byte  = 8 500
    NB_envoi = 20 000 / 8 500 ≈ 2,35 
    2,35 Arrondi au Supp = 3
        -> 3
        -> S

    // La longueur byte correspond aux nb de charactères envoyer en même temps
    hexa = "11122233344" et --byte = 3
        ~> 111
        ~> 222
        ~> 333
        ~> 44
    On envoie donc :
        -> 3
        -> S
    
    // La variable last_line_len permet de spécifier la longueur de la dernière ligne
    de la liste hexa
    hexa_list : ["111","222","333","44"]
    last_line_len est donc égal a 2
        -> 2
        -> S

    // L'envoie du fichier est une étape importante. En effet c'est là ou on va envoyer
    l'hexa du fichier
    """
    
    import socket
    import binascii
    import time
    print("--- Creating of client ---")
    print("Connection to the server :",args.ip)
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.connect((args.ip,args.port))

    #Envoie du nom du fichier
    len_ = len(args.file)
    for i in str(len_):
        socket.send(i.encode('utf-8'))
    socket.send(b'S')
    for i in args.file:
        socket.send(i.encode('utf-8'))

    #Ouvre le fichier en hexa
    file = open(str(args.file),'rb')
    content = file.read()
    file.close()
    hexa = str(binascii.hexlify(content))[2:-1]

    #Verif que byte est inférieur a len(hexa)
    if int(args.byte) > len(hexa):
        print("Little File, modification of byte")
        a = args.byte
        args.byte = len(hexa) - 2
        print(a, "->", args.byte)
    
    #Calcul du nombre d'envoie
    nb = len(hexa) / int(args.byte)
    if str(nb).split('.')[-1] == "0" :
        send_nb = int(nb)
    else :
        send_nb = int(str(nb).split('.')[0]) + 1
    print("Number File Send :",send_nb)

    #Envoie de send_nb (nombre d'envoie)
    for i in str(send_nb):
        socket.send(i.encode('utf-8'))
    socket.send(b"S")

    #Découpe de la vr hexa en liste
    hexa_list = []
    for i in range(0,send_nb):
        if i != send_nb - 1:
            hexa_list.append(str(hexa[i*args.byte:int(i*args.byte+args.byte)]))
        else :
            hexa_list.append(str(hexa[i*args.byte:]))
    
    #Envoie de la vr byte
    for i in str(args.byte):
        socket.send(i.encode('utf-8'))
    socket.send(b"S")

    #Envoie de la vr last_line_len
    for i in str(len(hexa_list[-1])):
        socket.send(i.encode('utf-8'))
    socket.send(b"S")

    print("Verif byte :",len(hexa_list[0]))
    
    #Envoie du fichier
    t = 0
    for i in hexa_list:
        socket.sendall(str(i).encode('utf-8'))
        print('Transfert :',int(t*100/(int(send_nb)-1)),"% ",progress_bar(14,"■","□",int(t*100/int(send_nb-1))),end='\r')
        t += 1
    print("Waiting 10 second ...                              ",end="\r")
    time.sleep(10)
    if len(hexa_list[-1]) == 1:
        socket.send(b"SS")
    else :
        socket.send(b"S")
    print("--- END ---                ")

def main(args):
    if args.role.lower() == "s":
        server(args)
    else :
        client(args)
if __name__ == "__main__":
    main(args)