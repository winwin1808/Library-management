import cv2 #pip install opencv-python
import pandas as pd #pip install pandas
import os #no need to install
from pyzbar.pyzbar import decode #pip install pyzbar 
from openpyxl import load_workbook #pip install openpyxl
import numpy as np
os.chdir("D:\LEARN\Python\Final_Project")

#detect clone Student card:
card = cv2.imread('Student_Card/STUDENT_CARD_00.jpg')
card = cv2.resize(card,(600,400))
card_copy = card.copy()
cardGray = cv2.cvtColor(card,cv2.COLOR_BGR2GRAY)
cardBlur = cv2.GaussianBlur(cardGray,(5,5),10)
cardCanny = cv2.Canny(cardGray,150,200)
countours,__ = cv2.findContours(cardCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(card,countours,-1,(0,255,0),1)

def rectangle_countours(countours):
    rect_cnts = []
    for c in countours:
        area = cv2.contourArea(c)
        # print(area)
        if area > 200:
            peri = cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,0.05*peri,True)
            # print(len(approx))
            if len(approx) == 4:
                rect_cnts.append(c)   
    rect_cnts = sorted(rect_cnts,key = cv2.contourArea,reverse=True)
    return rect_cnts
########################################################################
def get_conrner_point(c):
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.05*peri,True)
    return approx
########################################################################    
def four_points(points):
    points = points.reshape(4,2)
    new_points = np.zeros((4,1,2),dtype="float32")

    s = points.sum(axis = 1)
    new_points[0] = points[np.argmin(s)]
    new_points[3] = points[np.argmax(s)]
    print(s)
    diff = np.diff(points, axis = 1)
    new_points[1] = points[np.argmin(diff)]
    new_points[2] = points[np.argmax(diff)]
    print(diff)
    return new_points
########################################################################
rect_cnts = rectangle_countours(countours)
biggest_countours = get_conrner_point(rect_cnts[0])
if biggest_countours.size != 0:
    # cv2.drawContours(card,biggest_countours,-1,(255,0,0),20)
    # four_points(biggest_countours)
    biggest_countours = four_points(biggest_countours)

    point_1 = np.float32(biggest_countours)
    point_2 = np.float32([[0,0],[600,0],[0,400],[600,400]])

    matrix = cv2.getPerspectiveTransform(point_1,point_2)
    card_warp = cv2.warpPerspective(card,matrix,(600,400))


# code = decode(card_copy)
# id = code[0].data.decode('utf-8')
# pts = np.array([code[0].polygon],np.int32)
# print(pts)
# pts = pts.reshape((-1,1,2))
# cv2.polylines(card,[pts],True,(255,0,255),2)
# code = decode(card_warp)
# id = code[0].data.decode('utf-8')
# pts = np.array([code[0].polygon],np.int32)
# print(pts)
# pts = pts.reshape((4,1,2))
# cv2.polylines(card_warp,[pts],True,(255,0,255),2)
# # print(id)
cv2.imshow('card',card_warp)
cv2.imshow('cacgoc',card)
cv2.waitKey(0)