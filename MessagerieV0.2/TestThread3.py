from threading import Thread
import os

global ip3
ip3 = []

def ping(ip):
    print(ip)
    result = os.system(f"ping -c 1 -t 1 {ip}")
    if result == 0 :
        ip3.append(ip)
#liste des threads
ls_thread = []
for ip in range(255):
    ip2 = f"192.168.1.{ip}"
    ls_thread.append(Thread(target=ping,args=[ip2])) #Mettre en [] si 1 arg sinon (arg1,arg2)

print('...')

for th in ls_thread :
    th.start()

for th in ls_thread :
    th.join()

for i in ip3 : print(i)
print("Fin du programme")
