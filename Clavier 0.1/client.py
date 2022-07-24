"""
Execute this code on the Tablette/Phone/Ipad
"""
from tkinter import *
from functools import partial
import socket

def send(lettre,socket):
    socket.send(lettre.encode('utf8'))

Host = input("Ip (write when you execute server.py) :")
Port = 6969

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((Host,Port))

coef_size = 10

window = Tk()

window.title("Clavier 0.1")
window.geometry(f"{coef_size*100}x{int(coef_size/3)*100}")
window.minsize(coef_size*100,int(coef_size/3)*100)
window.maxsize(coef_size*100,int(coef_size/3)*100)

i = 0
for lettre in list("AZERTYUIOP"):
    action_with_arg = partial(send, lettre, socket)
    Button(window,height=int(coef_size*0.5),width=int(coef_size*0.95),text=lettre,command=action_with_arg).grid(row=0,column=i)
    Label(window,width=int(coef_size*0.19)).grid(row=0,column=i+1)
    i += 2
Label(window,height=int(coef_size*0.01)).grid(row=1,column=0)
i = 0
for lettre in list("QSDFGHJKLM"):
    action_with_arg = partial(send, lettre, socket)
    Button(window,height=int(coef_size*0.5),width=int(coef_size*0.95),text=lettre,command=action_with_arg).grid(row=2,column=i)
    i += 2
Label(window,height=int(coef_size*0.01)).grid(row=3,column=0)
i = 0
for lettre in list("WXCVBN"):
    action_with_arg = partial(send, lettre, socket)
    Button(window,height=int(coef_size*0.5),width=int(coef_size*0.95),text=lettre,command=action_with_arg).grid(row=4,column=i)
    i += 2
window.mainloop()


