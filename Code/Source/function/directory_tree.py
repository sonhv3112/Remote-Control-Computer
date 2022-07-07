from genericpath import isfile
import os
import shutil
from function.utilities import *

DF_MIDDLE   = '├─ '
DF_LAST     = '└─ '
PAR_MIDDLE  = '|&nbsp;&nbsp;'
PAR_LAST    = '&nbsp;&nbsp;&nbsp;'

# element = (name, depth, isLast)
def list2DirTree(list):  
    res = []
    statPar = []
    for (name, depth, isLast) in list: 
        if (depth == 0): 
            res.append(name)
            continue 
        line = ''
        if (len(statPar) < depth): 
            statPar.append(0) 
        statPar[depth - 1] = isLast
        for i in range(depth - 1): 
            line += PAR_LAST if (statPar[i]) else PAR_MIDDLE
        line += DF_LAST if (isLast) else DF_MIDDLE
        line += name
        res.append(line)
    return res 

def listTree(path, isRoot = 1):
    if (not os.path.isdir(path)): 
        return [('Folder does not exists', 0, True)]
    list = [] 
    if (isRoot): 
        list.append((path, 0, True))
    try: 
        current_dir = os.listdir(path)
    except: 
        return list
    for i in range(len(current_dir)): 
        current_path = os.path.join(path, current_dir[i])
        list.append((current_dir[i] + ('/' if (os.path.isdir(current_path)) else ''), 1, i == len(current_dir) - 1))
        if (os.path.isdir(current_path)): 
            try: 
                os.listdir(current_path) 
            except: 
                continue
            tlist = listTree(current_path, 0)
            for (name, depth, isLast) in tlist: 
                list.append((name, depth + 1, isLast))  
    return list 

def listDir(path): 
    if (not os.path.isdir(path)): 
        return [('Folder does not exists')]
    list = [(path, 0, True)]
    try: 
        os.listdir(path) 
    except: 
        return list
    if (len(os.listdir(path)) == 0): 
        list.append([('Folder is empty', 0, True)])
    else: 
        for d in os.listdir(path): 
            list.append((d, 1, False))
        list[-1] = (list[-1][0], list[-1][1], True)
    return list 


def listDisk(): 
    list = [('This PC', 0, True)] 
    for i in range(ord('A'), ord('Z') + 1): 
        if (os.path.isdir(f'{chr(i)}:/')): 
            list.append((f'{chr(i)}:/', 1, False))
    list[-1] = (list[-1][0], list[-1][1], True)
    return list 

def deleteDF(path):
    if (os.path.isdir(path)): 
        try: 
            shutil.rmtree(path) 
            return [('Delete folder successful!', 0, True)]
        except: 
            return [('Delete folder failed!', 0, True)]
    elif (os.path.isfile(path)): 
        try: 
            os.remove(path) 
            return [('Delete file successful!', 0, True)]
        except: 
            return [('Delete file failed!', 0, True)]
    return [('Delete failed!', 0, True)]

def copy(src, dst): 
    if (os.path.isdir(src)): 
        try: 
            shutil.copytree(src, dst)  
            return [('Copy folder successful!', 0, True)]
        except: 
            return [('Copy folder failed!', 0, True)]
    elif (os.path.isfile(src)): 
        try: 
            shutil.copy(src, dst)  
            return [('Copy file successful!', 0, True)]
        except: 
            return [('Copy file failed!', 0, True)]
    return [('Copy failed!', 0, True)]

def handle_directory(server, request, msg): 
    request = request.strip()
    if ('LIST_DISK' in request): 
        server.send_msg('REPLY DIRECTORY LIST DISK', [(listLine2HTML(list2DirTree(listDisk())), 'html')])
    elif ('LIST_TREE' in request): 
        path = request.split()[-1]
        server.send_msg('REPLY DIRECTORY LIST TREE', [(listLine2HTML(list2DirTree(listTree(path))), 'html')])
    elif ('LIST_DIR' in request): 
        path = request.split()[-1]
        server.send_msg('REPLY DIRECTORY LIST DIR', [(listLine2HTML(list2DirTree(listDir(path))), 'html')])
    elif ('DELETE' in request): 
        path = request.split()[-1]
        server.send_msg('REPLY DIRECTORY DELETE', [(listLine2HTML(list2DirTree(deleteDF(path))), 'html')])
    elif ('SAVE_FILE' in request): 
        path = request.split()[-1]
        check = server.download_file(msg, path)
        server.send_msg('REPLY DIRECTORY SAVE FILE', [(listLine2HTML(['Save file succesful!' if check else 'Save file failed!']), 'html')])
    elif ('COPY' in request): 
        src, dst = request.split()[-2:] 
        server.send_msg('REPLY DIRECTORY COPY', [(listLine2HTML(list2DirTree(copy(src, dst))), 'html')])

        

