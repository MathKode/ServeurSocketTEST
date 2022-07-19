import socket
import ssl

#Setting
def ip():
    hostname=socket.gethostname()
    your_ip=socket.gethostbyname(hostname)
    print("Server local IP :",your_ip)
    return str(your_ip)
host = ip()
port = 10500
socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Start Server
socket_obj.bind((host,port))
socket_obj.listen(5)
print("Serveur Up")

#Load the Server Certificate and his private key
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain("CERT/cert-server.pem","CERT/cert-key.pem")

#Secure Server by ssl
server_ssl = context.wrap_socket(socket_obj, server_side=True)

#Accept Connection
client_ssl, _ip = server_ssl.accept()
print(f"Cient ip : {_ip}")

while True:
    try:
        #Send message
        msg=str(input("Server : ")).encode()
        client_ssl.send(msg)    

        #Get message
        msg=client_ssl.recv(1024).decode()
        print(f"Client : {msg}")
    except:
        break

print("-- END --")
client_ssl.close()
server_ssl.close()
socket_obj.close()