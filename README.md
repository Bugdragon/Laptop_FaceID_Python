# Laptop_FaceID_Python
使用Python实现基于face_recognition的笔记本电脑人脸识别

### 安装指南
* git clone https://github.com/Bugdragon/Laptop_FaceID_Python.git
* 人脸图像命名 myface.jpg
* python FaceID_v2.0.py
* pyinstaller --hidden-import=queue -w -F FaceID_v2.0.py --noconsole 可生成.exe

### 版本条件
* Windows   10
* Python    3.7.1
* dlib      19.16.0
* numpy     1.15.4
* Click     7.0
* Pillow    5.3.0
* pyautogui 0.9.41
* PyInstaller     3.4
* opencv-python   3.4.3.18
* face-recognition          1.2.3
* face-recognition-models   0.3.0
