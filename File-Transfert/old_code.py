import argparse

parser = argparse.ArgumentParser(description='This code has been created to send a file between two PC on the local net')

parser.add_argument('-r','--role',metavar="[S]erver or [C]lient",type=str,help='The role of the machine where the code is running')
parser.add_argument('-i','--ip',metavar='SERVER IP',type=str,help="The IP of the server machine")
parser.add_argument('-f','--file',metavar='name',default=None,type=str,help="The name of the file")
parser.add_argument('-p','--port',type=int,default=5746,help="The Port of the server (optionnal)")

args = parser.parse_args()

def server(args):
    import binascii
    import socket
    import os

    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.bind((args.server,args.port))
    socket.listen(1)

    client, addr = socket.accept()
    print("Connection set up with :",addr)

    #Reception de la taille du fichier chiffre après chiffre
    size = ""
    while True: # Ex : 234 -> 2 puis 3 puis 4 puis S (pour signifier l'arrêt du code)
        reception = client.recv(1).decode('utf-8')
        if not reception or reception == 'S':
            break
        else :
            size += reception
    print("The size of the file is :",size)

    file = ""
    for i in range(int(size)):
        reception = client.recv(1).decode('utf-8')
        print('Transfert :',int(i*100/int(size)),"%",end='\r')
        if not reception :
            print('ERROR : The client has bugged')
            break
        else :
            file += reception
    print("Transfert END    ")

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
    
    if name == '' :
        print('ERROR with the transfert of the name')
        name = input('Put the name yourself : ')
    hexa = binascii.unhexlify(file)
    file = open(name,'wb')
    file.write(hexa)
    file.close()

    client.close()
    socket.close()
        

def client(args):
    import binascii
    import socket
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.connect((args.server,args.port))
    file = open(str(args.file),'rb')
    content = file.read()
    file.close()
    hexa = str(binascii.hexlify(content))[2:-1]
    print('File size :',len(hexa))
    size = str(len(hexa)) + "S"
    for i in size :
        socket.send(i.encode('utf8'))
    size = size[:-1]
    t = 0
    for i in hexa:
        print('Transfert :',int(t*100/int(size)),"%",end='\r')
        socket.send(i.encode('utf8'))
        t += 1
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
