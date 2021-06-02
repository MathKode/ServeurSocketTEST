from threading import Thread, current_thread
import time

class MyProcess(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range(5):
            print(current_thread(),i)
            time.sleep(0.1)

#déclare les threads
thread_1 = MyProcess()
thread_2 = MyProcess()

#Demare l'action d'un thread (appelle la fonction run)
thread_1.start()
thread_2.start()

#Stope le programme jusqu'a ce que les thread soit fini :
thread_1.join()
thread_2.join()

print('Fin du Programme')