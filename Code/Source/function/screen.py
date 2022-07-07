import cv2
import numpy as np
import pyautogui
import time
import io
from datetime import datetime

LOG_PATH = 'log/'

def take_screen():
    screenshot = pyautogui.screenshot()
    img_bytes = io.BytesIO() 
    screenshot.save(img_bytes, format='PNG') 
    return img_bytes.getvalue() 

def capture_screen(n_seconds, fps = 10, dim = (1920, 1080)):
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(LOG_PATH + 'capture.mp4', fourcc, fps, dim)
    for i in range(fps * n_seconds): 
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video.write(frame)
        time.sleep(1.0 / fps) 
    video.release()
    f = open(LOG_PATH + 'capture.mp4', 'rb') 
    video_bytes = f.read()
    f.close() 
    return video_bytes

def handle_screen(server, request, screenInfo): 
    request = request.strip()
    if ('TAKE' in request): 
        server.send_msg('REPLY SCREEN TAKE', [(take_screen(), f'{datetime.now().strftime("%d%m%Y_%H%M%S")}_screenshot.png')])
    elif ('CAPTURE' in request): 
        n_seconds = int(request.split()[-1])
        server.send_msg('REPLY SCREEN CAPTURE', [(capture_screen(n_seconds, dim = screenInfo), f'{datetime.now().strftime("%d%m%Y_%H%M%S")}_capture.mp4')])