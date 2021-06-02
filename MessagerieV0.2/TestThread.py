from threading import Thread
import time

def process_one():
    for i in range(5):
        print('oooooooooo',i)
        time.sleep(0.1)

def process_two():
    for i in range(5):
        print('xxxxxxxxxx',i)
        time.sleep(0.1)

#déclare un thread
thread_1 = Thread(target=process_one)
thread_2 = Thread(target=process_two)

#Demare l'action d'un thread
thread_1.start()
thread_2.start()

#Stope le programme jusqu'a ce que les thread soit fini :
thread_1.join()
thread_2.join()

print('Fin du Programme')