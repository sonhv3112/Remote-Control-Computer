import cv2
import numpy as np
import time
import io
from datetime import datetime

LOG_PATH = 'log/'

def record_camera(n_seconds, fps = 10):
    camera = cv2.VideoCapture(0)
    dim = ( int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), 
            int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))) 
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(LOG_PATH + "camera.mp4", fourcc, fps, dim)
    for i in range(fps * n_seconds): 
        ret, frame = camera.read() 
        video.write(frame) 
        time.sleep(1.0 / fps) 
    video.release() 
    f = open(LOG_PATH + 'camera.mp4', 'rb') 
    video_bytes = f.read()
    f.close() 
    return video_bytes

def handle_camera(server, request): 
    request = request.strip() 
    n_seconds = int(request.split()[-1])
    server.send_msg('REPLY RECORD CAMERA', [(record_camera(n_seconds), f'{datetime.now().strftime("%d%m%Y_%H%M%S")}_camera.mp4')])