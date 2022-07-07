import os

def shutdown():
    os.system('shutdown -s -t 3')

def restart():
    os.system('shutdown -r -t 3')

def logout(): 
    os.system('shutdown -l')
    