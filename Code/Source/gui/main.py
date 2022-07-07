from genericpath import exists
from importlib.resources import path
from pathlib import Path
from tkinter import Tk, Button, Label, simpledialog, messagebox
from PIL import ImageTk, Image
from cv2 import repeat
import pystray
import sys
import os
from threading import Thread
import random

ASSETS_PATH = 'assets/'
CONFIGS_FILE = 'configs.txt'

sys.path.insert(1, '/path/to/server/function/')
from function.listener import Listener
import function.keylogger as key

def mainWindow(SMTP_HOST, IMAP_HOST, SERVER_ADDRESS, SERVER_PASSWORD):
    gui = MainWindow(SMTP_HOST, IMAP_HOST, SERVER_ADDRESS, SERVER_PASSWORD)
  
    if gui.status != -1:
        gui.root.mainloop()

class MainWindow():
    """This class generates the GUI""" 

    def __init__(self, SMTP_HOST, IMAP_HOST, SERVER_ADDRESS, SERVER_PASSWORD): 
        self.screenInfo = self.getScreenInfo()
        self.listener = Listener(SMTP_HOST, IMAP_HOST, SERVER_ADDRESS, SERVER_PASSWORD, self.screenInfo)
        self.loadID()
        self.status = 0 - ('--startup' in sys.argv) 
        self.listening()

        if self.status == 0:
            self.generateMain()
        else:
            self.generateIcon()
            self.icon.run()

    def generateMain(self):
        self.root = Tk()
        self.width, self.height = 300, 300
        self.root.geometry(str(self.width) + 'x' + str(self.height))
        self.root.configure(bg = "#FFFFFF")
        self.root.title('Mail Remote Server')
        self.root.iconbitmap(ASSETS_PATH + 'icon.ico')
        self.root.protocol('WM_DELETE_WINDOW', self.withdrawWindow)
        self.root.resizable(False, False)
        self.generateText()
        self.generateButton()
        self.modifyStatus()

    def generateText(self):
        self.root.id1 = Label(
            text = "ID:",
            foreground="#545563",
            background="#FFFFFF",
            font = ("Segoe UI Black", 24 * -1, 'bold'),
        )

        self.root.id1.place(
            x = self.width // 5 * 1.7,
            y = self.height // 6 * 0.8,
            width = 150,
            height = 60,
            anchor = "center"
        )
        self.root.id2 = Label(
            text = self.ID,
            foreground="#545563",
            background="#FFFFFF",
            font = ("Segoe UI Black", 24 * -1, 'bold'),
        )

        self.root.id2.place(
            x = self.width // 5 * 3.5,
            y = self.height // 6 * 0.8,
            width = 150,
            height = 60,
            anchor = "center"
        )

        self.root.status1 = Label(
            text = "Status:",
            foreground="#545563",
            background="#FFFFFF",
            font = ("Segoe UI Black", 24 * -1, 'bold'),
        )

        self.root.status1.place(
            x = self.width // 5 * 1.7,
            y = self.height // 6 * 1.8,
            width = 150,
            height = 60,
            anchor = "center"
        )

        self.root.status2 = Label(
            text = "OFF",
            foreground="#FF5C60",
            background="#FFFFFF",
            font = ("Segoe UI Black", 24 * -1, 'bold'),
        )

        self.root.status2.place(
            x = self.width // 5 * 3.5,
            y = self.height // 6 * 1.8,
            width = 50,
            height = 60,
            anchor = "center"
        )

    def generateButton(self):
        self.root.statusButton = Button(
            background="#EDEEF2",
            foreground="#545563",
            activeforeground="#4E60FF",
            text = "Turn On",
            font = ("Segoe UI Black", 24 * -1, 'bold'),
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changeStatus(),
            relief="flat"
        )

        self.root.statusButton.place(
            x = self.width // 2,
            y = self.height // 6 * 3.2,
            width = 150,
            height = 60,
            anchor = "center"
        )

        self.root.changeIDButton = Button(
            background="#EDEEF2",
            foreground="#545563",
            activeforeground="#4E60FF",
            text = "Custom ID",
            font = ("Segoe UI Black", 24 * -1, 'bold'),
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.changeID(),
            relief="flat"
        )

        self.root.changeIDButton.place(
            x = self.width // 2,
            y = self.height // 6 * 4.8,
            width = 150,
            height = 60,
            anchor = "center"
        )
    def modifyStatus(self):
        if self.status == 0:
            self.root.statusButton.configure(text="Turn On")
            self.root.status2.configure(text="OFF", foreground="#FF5C60")
        else:
            self.root.statusButton.configure(text="Turn Off")
            self.root.status2.configure(text="ON", foreground="#7CFC00")

    def changeStatus(self): 
        self.status = 1 - self.status
        self.modifyStatus()

    def changeID(self): 
        if (self.status != 0):
            msg = messagebox.showerror("Server is listening", "Please turn off server before change ID.")
            return

        newID = simpledialog.askstring("Custom ID", "Enter your custom id:")
        while newID is None or newID == '' or self.listener.create_ID(newID) == False:
            msg = messagebox.showerror("Custom ID", "Sorry, ID already exists. Please try with another one.")
            newID = simpledialog.askstring("Custom ID", "Enter your custom id:")
        
        self.listener.delete_ID(self.ID)
        self.ID = newID
        self.saveID()
        self.root.id2.configure(text=self.ID)
        
    def quitWindow(self, icon, item):
        self.icon.stop()
        self.listenerStatus = 0
        if self.status != -1:
            self.root.destroy()

    def openWindow(self, icon, item):
        self.icon.stop()
        if self.status != -1:
            self.root.deiconify()
        else:
            self.status = 1
            self.generateMain()

    def generateIcon(self):
        image = Image.open(ASSETS_PATH + 'icon.ico')
        menu = (pystray.MenuItem('Open Mail Remote Server', self.openWindow), pystray.MenuItem('Quit Mail Remote Server', self.quitWindow))
        self.icon = pystray.Icon("Mail Remote Server", image, "Mail Remote Server", menu)

    def withdrawWindow(self):  
        self.root.withdraw()
        self.generateIcon()
        self.icon.run()

    def start(self):
        while self.listenerStatus:
            if self.status != 0:
                self.listener.recv_msg()
        key.flag = 4

    def listening(self):
        self.listenerStatus = 1
        self.listenerThread = Thread(target = self.start)
        self.listenerThread.start()

    def getRandomID(self):
        ID = str(random.randint(100000, 999999))
        while self.listener.create_ID(ID) == False:
            ID = str(random.randint(100000, 999999))
        return ID
    
    def saveID(self):
        f = open(CONFIGS_FILE, 'w')
        f.write('id=' + str(self.ID))
    
    def loadID(self):
        if os.path.exists(CONFIGS_FILE) == False:
            self.ID = self.getRandomID()
            self.saveID()
            return 
        f = open(CONFIGS_FILE, 'r')
        str = f.read()
        ID = str[str.find('=') + 1:]
        if ID == '':
            self.ID = self.getRandomID()
            self.saveID()
            return
        
        self.ID = ID
        self.listener.ID = ID

    def getScreenInfo(self):
        tmp = Tk()
        tmp.withdraw()
        screenInfo = (tmp.winfo_screenwidth(), tmp.winfo_screenheight())
        tmp.destroy()
        return screenInfo

        