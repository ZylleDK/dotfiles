#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import rospy
from std_msgs.msg import String
import json
import imutils
from Display import Display

def takeandsave():
    img_addr = 'http://192.168.0.20/image/jpeg.cgi'
    cap = cv2.VideoCapture(img_addr)
    if(cap.isOpened()):
        success, img= cap.read()
        cv2.imwrite('frame.jpg', img)
        cap.release()
    return

#def calibrate(h,w):
    #hwcali = 0.13157895 # cm/p
 #   hcm = 5/h#*hwcals
 #   wcm = 5/w#*hwcali
 #   return hcm, wcm

def block_position(b1,b2,b3):
# for left most position
    if b1["X"] < (b2["X"] and b3["X"]):
        b1["pos"] = "l"
    elif b2["X"] < (b1["X"] and b3["X"]):
        b2["pos"] = "l"
    elif b3["X"] < (b2["X"] and b1["X"]):
        b3["pos"] = "l"

# for middle most position
    if (b2["X"] < b1["X"] < b3["X"]) or (b3["X"] < b1["X"] < b2["X"]):
        b1["pos"] = "m"
    elif (b1["X"] < b2["X"] < b3["X"]) or (b3["X"] < b2["X"] < b1["X"]):
        b2["pos"] = "m"
    elif (b2["X"] < b3["X"] < b1["X"]) or (b1["X"] < b3["X"] < b2["X"]):
        b3["pos"] = "m"

# for right most positio
    if b1["X"] > (b2["X"] and b3["X"]):
        b1["pos"] = "r"
    elif b2["X"] > (b1["X"] and b3["X"]):
        b2["pos"] = "r"
    elif b3["X"] > (b2["X"] and b1["X"]):
        b3["pos"] = "r"



    return b1,b2,b3


def getcolorblock(img):
    img_hold = img
    img_hold2 = cv2.cvtColor(img_hold,cv2.COLOR_BGR2HSV)
    lower = np.array([10,10,100]) #[20,30,190]
    upper = np.array([100,255,255])
    mask = cv2.inRange(img_hold2,lower,upper)
    result = cv2.bitwise_and(img_hold,img_hold,mask=mask)
    return result

def getcenter(cnts):
    contor_counter= 0
    json_object_1={}
    json_object_2={}
    json_object_3={}
    for c in cnts:
#calculate moments of binary image
        M = cv2.moments(c)
        
# calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        (x,y,h,w)= cv2.boundingRect(c)
        contor_counter=contor_counter+1
        if contor_counter==1:
            json_object_1 = {"X": cX,
                             "Y": cY,
                             "h": h,
                             "w": w,
                             "pos": "u",
                             "command": "pickup"}

        elif contor_counter==2:
            json_object_2 = {"X": cX,
                             "Y": cY,
                             "h": h,
                             "w": w,
                             "pos": "u",
                             "command": "pickup"}
        elif contor_counter==3:
            json_object_3 = {"X": cX,
                             "Y": cY,
                             "h": h,
                             "w": w,
                             "pos": "u",
                             "command": "pickup"}
        else:
            print("more than 3 contours")

    return json_object_1,json_object_2,json_object_3

def pick_target(ob1,ob2,ob3, target):

    if ob1["pos"] == target:
        target_obj = ob1
        p1 = ob2
        p2 = ob3

    elif ob2["pos"] == target:
        target_obj = ob2
        p1 = ob1
        p2 = ob3

    elif ob3["pos"] == target:
        target_obj = ob3
        p1 = ob1
        p2 = ob2

    json_holder = {"T": [target_obj,p1,p2]}
    print(json_holder)

    return json_holder

def image_analyse():

# Create window to display images.
    window = Display('window1')
    window.resize(800, 600)
    takeandsave()
    img = cv2.imread('frame.jpg')
    img[0:83]=[0] #set upper parts of image to 0 to only keep blob
    img[260:479]=[0] #set lower parts of image to 0 to only keep blob
#window.update(img)
#cv2.waitKey(0)

#extract color block
    img2 = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    img3=getcolorblock(img2)
#window.update(img3)
#cv2.waitKey(0)
#
    img4 = cv2.cvtColor(img3, cv2.COLOR_HSV2BGR)
    img5 = cv2.cvtColor(img4, cv2.COLOR_BGR2GRAY)
#window.update(img5)
#cv2.waitKey(0)
    ret,thresh = cv2.threshold(img5,5,255,0) #create binary image
    thresh[260:479]=[0] #set lower parts of image to 0 to only keep blob
#
    _,contours1, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
#window.update(thresh)
#cv2.waitKey(0)
#
    img7 = cv2.fillPoly(thresh, contours1, color=(255,255,255))
#window.update(img7)
#cv2.waitKey(0)
#
    _,contours2, hierarchy = cv2.findContours(img7, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    img8 = cv2.drawContours(img7, contours2, -1, (0,255,0),3) #-1 draw all countors, 2nd is color of contor and third is thickness
#window.update(img8)
#cv2.waitKey(0)
#
    cons = cv2.findContours(img8, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cons)
    con1,con2,con3 = getcenter(cnts)
    #hcm, wcm = calibrate(h,w)
    window.update(img8)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return con1,con2,con3


def blockinformation(staple_block):
        print(command)
        block1,block2,block3 = image_analyse()
        b1n, b2n, b3n=block_position(block1,block2,block3)
        target_object= pick_target(b1n, b2n, b3n, staple_block)
        target_obj_string = json.dumps(target_object)
       # rospy.loginfo(json_string)
        pub.publish(target_obj_string)
        rate.sleep()

if __name__ == '__main__':
    command = raw_input("enter l,m or r to staple the blocks on top of asked block: ")
    print(command)
    pub = rospy.Publisher('blockinfo', String, queue_size=10)
    rospy.init_node('blockinfogetter', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        raw_input("Press Enter to calculate and send image data!")
        blockinformation(command)

