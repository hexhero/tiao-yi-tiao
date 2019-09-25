'''
半个小时的成果, 代码比较乱
'''

import cv2
import numpy as np
import math,os,time

# 距离转时间系数
DTC = 0.208 
# 手机屏幕缩放比例
SCA = 0.3

def update_img():
    os.system('adb shell screencap /sdcard/screen.png')
    time.sleep(1)
    os.system('adb pull /sdcard/screen.png')
    time.sleep(2)

def get_res():
    img = cv2.imread('screen.png')
    res = cv2.resize(img,None,fx=SCA, fy=SCA, interpolation = cv2.INTER_CUBIC)
    return res

update_img();
res = get_res()

start_point = [0,0];
end_point = [0,0];
flag = 0;

def jump():
    width = math.fabs(start_point[0]-end_point[0]);
    height = math.fabs(start_point[1]-end_point[1]);
    length = math.sqrt(width**2 + height**2);
    print("length %s" % length)
    os.system('adb shell input swipe 400 1200 400 1200 %s' % int(length/DTC))
    time.sleep(1)

def click_event(event,x,y,flags,param):
    global flag
    global res
    if event == cv2.EVENT_LBUTTONDOWN:
        if flag == 0:
            start_point[0] = x
            start_point[1] = y
            flag = 1
        elif flag == 1:
            end_point[0] = x
            end_point[1] = y
            print(start_point,end_point)
            jump()
            update_img()
            res = get_res()
            flag = 0

cv2.namedWindow('image')
cv2.setMouseCallback('image',click_event)
while(1):
    cv2.imshow('image',res)
    if cv2.waitKey(20) & 0xFF == 27:
        break
cv2.destroyAllWindows()