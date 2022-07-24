import argparse

parser = argparse.ArgumentParser(description='This code has been created to send a file between two PC on the local net')

parser.add_argument('-r','--role',metavar="[S]erver or [C]lient",type=str,help='The role of the machine where the code is running')

args = parser.parse_args()

def server(args):
    import socket
    import time

    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.bind(("192.168.1.27",7832))
    socket.listen(1)

    client, addr = socket.accept()
    print("Connection set up with :",addr)

    size = ""
    while True: # Ex : 234 -> 2 puis 3 puis 4 puis S (pour signifier l'arrêt du code)
        reception = client.recv(1).decode('utf-8')
        if not reception or reception == 'S':
            break
        else :
            size += reception
    print("The size of the file is :",size)
    
    msg = client.recv(int(size)).decode('utf8')
    print(len(msg))

    client.close()
    socket.close()
        

def client(args):
    import binascii
    import socket
    socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.connect(("192.168.1.27",7832))
    
    hexa = "a"*131020 # <------------- 131 020 est le nombre de lettre max que l'on peut envoyer en une connection

    size = str(len(hexa)) + "S"
    for i in size :
        socket.send(i.encode('utf8'))
    
    socket.send(hexa.encode('utf8'))
    

def main(args):
    if str(args.role).lower() == "s":
        server(args)
    else :
        client(args)

if __name__ == "__main__":
    main(args)