'''
优化：
使用multiprocessing多线程处理识别程序
'''
import pyautogui
import os
import traceback
from multiprocessing import Process, Pipe
#from subprocess import call
from ctypes import *
from threading import Timer
import cv2
import face_recognition
import numpy as np

LOCK_TIMEOUT = 0.01 # 锁屏计时时间
UNLOCK_TIMEOUT = 0.01 # 解锁延迟时间
#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = './'
'''
SCREENSAVER_COMMAD = 'cinnamon-screensaver-command'
LOCK_ARGS = {
    True: '--activate',
    False: '--deactivate',
}
'''

# 锁屏
def lock_screen(lock):
    if lock:
        user32 = windll.LoadLibrary('user32.dll')
        user32.LockWorkStation()
    else:
        pyautogui.press('enter')
        #pyautogui.click(944, 668) # 1080p
        #pyautogui.press('1')
        #pyautogui.press('1')
        #pyautogui.press('8')
        #pyautogui.press('1')
        #pyautogui.press('2')
        #pyautogui.press('4')

    #call((SCREENSAVER_COMMAD, LOCK_ARGS[lock]))

#lock_screen(True) # 锁屏
#lock_screen(False) # 解锁屏

# 加载我的人脸
def load_myface_encoding():
    try:
        my_image_face_encoding = np.load(os.path.join(BASE_DIR, 'myface'))
    except FileNotFoundError:
        my_image = face_recognition.load_image_file(os.path.join( BASE_DIR, 'myface.jpg'))
        my_image_face_encoding = face_recognition.face_encodings(my_image, num_jitters=10)[0]
        np.save(os.path.join(BASE_DIR, 'myface'), my_image_face_encoding)
    
    return my_image_face_encoding

# 人脸比对
def find_myface_in_frame(conn, frame, myface_encoding):
    face_locations = face_recognition.face_locations(frame, model='cnn') # 构造神经网络来定位框架中的面部
    face_encodings = face_recognition.face_encodings(frame, face_locations, num_jitters=2)
    
    found_myface = False
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces((myface_encoding,), face_encoding, tolerance=0.9)

        found_myface = any(matches)
        if found_myface:
            break

    conn.send(found_myface)

def main():
    myface_encoding = load_myface_encoding()
    video_capture = cv2.VideoCapture(0) # 获取视频流

    lock_timer = None
    find_myface_process = None
    parent_conn, child_conn = Pipe()

    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1] # HxWxC | BGR -> RGB

        if find_myface_process is None:
            find_myface_process = Process(target=find_myface_in_frame, args=(child_conn, rgb_small_frame, myface_encoding))
            find_myface_process.start()
        elif find_myface_process is not None and not find_myface_process.is_alive():
            myface_found = parent_conn.recv()
            find_myface_process = None

            if myface_found:
                print('face found!')
                lock_screen(False)

                if lock_timer is not None: # 取消锁定计时
                    lock_timer.cancel()
                    lock_timer = None
                    118124
                    118124

            else:
                print('face not found!')

                if lock_timer is None: # 开始锁定计时
                    lock_timer = Timer(LOCK_TIMEOUT, lock_screen, (True,)) # 开启锁屏计时
                    lock_timer.start()

if __name__ == '__main__':
    while True:
        try:
            main()
        except Exception:
            with open(os.path.join(BASE_DIR, 'error.log'), 'a') as error_file:
                traceback.print_exc(file=error_file)
                error_file.write('\n')