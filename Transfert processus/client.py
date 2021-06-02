import socket
import subprocess

serveur_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Host = "192.168.1.27"
Port = 1234
serveur_client.connect((Host,Port))
while True:
    process = str(subprocess.check_output(["ps","-e"]).decode('utf8'))
    serveur_client.send(process.encode("UTF-8"))