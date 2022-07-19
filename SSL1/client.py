import socket
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

#Load le CA CERT
context.load_verify_locations("CA/ca-cert.pem")

#Setting
host = str(input("Server IP : "))
port = 10500
socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Securisation du socket
client_ssl=context.wrap_socket(socket_obj, server_hostname=host)
client_ssl.connect((host, port))

while True:
    #Get message
    msg=client_ssl.recv(1024).decode()
    print(f"Server : {msg}")

    #Send message
    msg=str(input("Client : ")).encode()
    client_ssl.send(msg)    