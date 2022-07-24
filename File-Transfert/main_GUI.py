from tkinter import *
from tkinter import ttk
import mainV2
import os

class PARSER:
    def __init__(self,role,ip,file,port,byte) :
        self.role = str(role)
        self.ip = str(ip)
        self.file = str(file)
        self.port = int(port)
        self.byte = int(byte)

def click_c1():
    c2.deselect()
def click_c2():
    c1.deselect()

def start():
    if int(c1_vr.get()) == 0:
        args = PARSER("s",ip_input.get(),file_combobox.get(),port_input.get(),byte_input.get())  
    else :
        args = PARSER("c",ip_input.get(),file_combobox.get(),port_input.get(),byte_input.get()) 
    txt = console["text"]
    console.config(text=f"{txt}\nSTARTING : Send the File")
    try :
        mainV2.main(args)
        txt = console["text"]
        console.config(text=f"{txt}\nSending successfully :-)")
    except :
        print("Erreur")
        txt = console["text"]
        console.config(text=f"{txt}\nERREUR : sending fail  ...")


def help():
    help = Tk()
    help.title("File Transfert HELP")
    help.geometry("500x200")
    help.minsize(500,200)
    help.maxsize(500,200)
    help.config(background="#BFBFBF")
    Label(help,text="""This code allow you to send a file between two PC connected on the same network
    To do this, you have to run him on the tow pc
    \nOnce this code run, choose the role of the PC : Server or Client
    \nAfter, put the ip of the server pc (do a ipconfig on windows and ifconfig on other)
    \nSet the port use by the socket (optionnal)
    \nIf you're the Client PC, choose a file
    \nSqueeze the start button of the Client PC before Server PC""").pack()
    help.mainloop()

def contact():
    c = Tk()
    c.title("File Transfert Contact")
    c.geometry("240x25")
    c.minsize(240,25)
    c.maxsize(240,25)
    c.config(background="#BFBFBF")
    Label(c,text="Email : bimathax.STUDIO@gmail.com").pack()
    c.mainloop()

windows = Tk()
windows.title("File Transfert")
windows.geometry("500x500")
windows.minsize(500,500)
windows.maxsize(500,500)
windows.config(background="#BFBFBF")

Label(windows,text="File Transfert",font="Arial 39 bold underline",bg="#BFBFBF",fg="#2457FE").pack()
Label(windows,text=" ",font="Arial 5 italic bold underline",bg="#BFBFBF",fg="#2457FE").pack()

frame = Frame(windows,bg="#BFBFBF")

global c1
global c1_vr
c1_vr = IntVar()
c1 = Checkbutton(frame,text="Envoyer\nClient", bg="#DCDBDB",fg="#2457FE",font="Consolas 15",onvalue=1, offvalue=0,width=20,variable=c1_vr,command=click_c1)
c1.grid(row=0,column=0)
space = Label(frame,width=3,bg="#BFBFBF",fg="#000000")
space.grid(row=0,column=1)

global c2
global c2_vr
c2_vr = IntVar()
c2 = Checkbutton(frame,text="Recevoir\nServeur", bg="#DCDBDB",fg="#2457FE",font="Arial 15",onvalue=1, offvalue=0,variable=c2_vr,width=20,command=click_c2)
c2.grid(row=0,column=2)
space.grid(row=1,column=1)
frame.pack()

frame_2 = Frame(windows, bg="#BFBFBF")

Label(frame_2,text="IP SERVER :",font="Arial 20 italic bold",bg="#BFBFBF",fg="#2457FE",anchor="nw",width=13).grid(row=0,column=0)
global ip_input
ip_input = Entry(frame_2)
ip_input.grid(row=0,column=1)
ip_input.insert(0,'192.168.#.#')

space2 = Label(frame_2,text="^",font="Arial 3",bg="#BFBFBF",fg="#BFBFBF")
space2.grid(row=1,column=0)

Label(frame_2,text="Port :",font="Arial 20 italic bold",bg="#BFBFBF",fg="#2457FE",anchor="nw",width=13).grid(row=2,column=0)
global port_input
port_input = Entry(frame_2)
port_input.grid(row=2,column=1)
port_input.insert(0,"5746")

space2 = Label(frame_2,text="^",font="Arial 3",bg="#BFBFBF",fg="#BFDFBF")
space2.grid(row=3,column=0)

Label(frame_2,text="Byte :",font="Arial 20 italic bold",bg="#BFBFBF",fg="#2457FE",anchor="nw",width=13).grid(row=4,column=0)
global byte_input
byte_input = Entry(frame_2)
byte_input.grid(row=4,column=1)
byte_input.insert(0,"8500")

space2 = Label(frame_2,text="^",font="Arial 3",bg="#BFBFBF",fg="#BFDFBF")
space2.grid(row=5,column=0)

Label(frame_2,text="File :",font="Arial 20 italic bold",bg="#BFBFBF",fg="#2457FE",anchor="nw",width=13).grid(row=6,column=0)
file = os.listdir()
global file_combobox
file_combobox = ttk.Combobox(frame_2,values=file,width=18)
file_combobox.grid(row=6,column=1)

frame_2.pack()

Label(windows,text="^",bg="#BFBFBF",fg="#BFBFBF").pack()
Button(windows,text="START",font="Arial 22 bold",command=start).pack()

Label(windows,text="^",bg="#BFBFBF",fg="#BFBFBF",height=2).pack()
global console
console = Label(windows,bg="#FFFFFF",fg="#000000",width=50,height=6,anchor="sw")
console.pack()

menu_bar = Menu(windows)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Contact", command=contact) 
file_menu.add_command(label="Help", command=help)
file_menu.add_command(label="Quitter", command=windows.quit)
menu_bar.add_cascade(label="Fichier", menu=file_menu)
windows.config(menu=menu_bar)

windows.mainloop()