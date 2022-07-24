"""
Execute this code on the Pc/Mac OS
"""
import socket
import keyboard
import os

if os.name == "nt" :
    #Windows
    cmd = os.popen("ipconfig")
    ip = cmd.read().split('Adresse IPv4. . . . . . . . . . . . . .: ')[1]
    ip = ip.split()[0]
else :
    #MacOs
    terminal = os.popen("ifconfig")
    ip = terminal.read().split("broadcast")[0]
    ip = str(ip[-60:].split('inet ')[1]).split(" ")[0]
print('Ton ip :',ip)

Host = ip
Port = 6969

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((Host,Port))
socket.listen(1)
client, ip = socket.accept()
print("Le clavier d'ip",ip,"s'est connecté")

while True:
    rep = client.recv(6).decode("utf8")
    print(rep)
    if not rep:
        break
    keyboard.write(rep)

client.close()
socket.close()
