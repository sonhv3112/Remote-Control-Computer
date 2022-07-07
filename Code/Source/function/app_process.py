import psutil
import os
from function.utilities import *

def list_apps():
    ls1 = list()
    ls2 = list()
    ls3 = list()

    cmd = 'powershell "gps | where {$_.mainWindowTitle} | select Description, ID, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}'
    proc = os.popen(cmd).read().split('\n')
    tmp = list()
    for line in proc:
        if not line.isspace():
            tmp.append(line)
    tmp = tmp[3:]
    for line in tmp:
        try:
            arr = line.split(" ")
            if len(arr) < 3:
                continue
            if arr[0] == '' or arr[0] == ' ':
                continue

            name = arr[0]
            threads = arr[-1]
            ID = 0
            # interation
            cur = len(arr) - 2
            for i in range (cur, -1, -1):
                if len(arr[i]) != 0:
                    ID = arr[i]
                    cur = i
                    break
            for i in range (1, cur, 1):
                if len(arr[i]) != 0:
                    name += ' ' + arr[i]
            ls1.append(name)
            ls2.append(ID)
            ls3.append(threads)
        except:
            pass
    return ls1, ls2, ls3


def list_processes():
    ls1 = list()
    ls2 = list()
    ls3 = list()
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            name = proc.name()
            pid = proc.pid
            threads = proc.num_threads()
            ls1.append(str(name))
            ls2.append(str(pid))
            ls3.append(str(threads))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return ls1, ls2, ls3

def kill(pid):
    cmd = 'taskkill.exe /F /PID ' + str(pid)
    try:
        a = os.system(cmd)
        if a == 0:
            return True
        else:
            return False
    except:
        return False
    
def start(name):
    try:
        os.system(name)
        return True 
    except:
        return False

def handle_app_process(server, request): 
    request = request.strip()
    if ('LIST_APPS' in request): 
        name, id, thread = list_apps()
        server.send_msg('REPLY PROCESS LIST APPS', [(listAP2HTML(name, id, thread, 'App'), 'html')])
    elif ('LIST_PROCESSES' in request): 
        name, id, thread = list_processes()
        server.send_msg('REPLY PROCESS LIST PROCESSES', [(listAP2HTML(name, id, thread, 'Process'), 'html')])
    elif ('KILL' in request): 
        pid = request.split()[-1] 
        check = kill(pid) 
        server.send_msg('REPLY PROCESS KILL', [(listLine2HTML(['Kill successfull' if (check) else 'Kill failed']), 'html')])
    elif ('START' in request): 
        name = request.split()[-1] 
        check = start(name) 
        server.send_msg('REPLY PROCESS START', [(listLine2HTML(['Start successfull' if (check) else 'Start failed']), 'html')])