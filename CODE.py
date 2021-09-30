import cv2 #pip install opencv-python
import pandas as pd #pip install pandas
import os #no need to install
from pyzbar.pyzbar import decode #pip install pyzbar 
from openpyxl import load_workbook #pip install openpyxl
import numpy as np
import glob
from mailer import Mailer #pip install quick-mailer
os.chdir("D:\LEARN\Python\Final_Project")

card_list = list()
book_list = list()

for name in glob.glob("Student_Card/*.jpg"): 
  card = cv2.imread(name)
  card_list.append(card)

for name in glob.glob("Book_List/*.jpg"): 
  book = cv2.imread(name)
  book_list.append(book)
########################################################################
student_data = pd.read_excel("DATA.xlsx", sheet_name = "Student data")
book_data = pd.read_excel("DATA.xlsx", sheet_name = "Book data")
book_data['CODE'] = book_data['CODE'].apply(lambda x: '{:.0f}'.format(x))
########################################################################
def student_card_detect(card):
    code = decode(card)
    id = code[0].data.decode('utf-8')
    for i in range(len(student_data)):
        if int(id) == int(student_data.loc[i,'Student_ID']):
            return(student_data.loc[i])
########################################################################
def book_detect(book):
    book_code = decode(book)
    code = book_code[0].data.decode('utf-8')

    for i in range(len(book_data)):
        if code == book_data.loc[i,'CODE']:
            return(book_data.loc[i])
########################################################################
def borrow_book(card_info, book_info):
    borrow_info = pd.DataFrame({'BOOK':book_info['BOOK'],'ID':card_info['Student_ID'],'Student_name':card_info['STUDENT']}, index = [0])
    return borrow_info

borrow_list = pd.DataFrame(columns=['BOOK','ID','Student_name'])  
borrow_list = borrow_list.append(borrow_book(student_card_detect(card_list[0]),book_detect(book_list[0])))
borrow_list = borrow_list.append(borrow_book(student_card_detect(card_list[0]),book_detect(book_list[1])))
borrow_list = borrow_list.append(borrow_book(student_card_detect(card_list[1]),book_detect(book_list[2])))

########################################################################
file = pd.ExcelWriter('DATA.xlsx', mode='a', if_sheet_exists = 'replace')
borrow_list.to_excel(file, 'Borrowed data')
file.save()
########################################################################
def get_book_info(book_name):
    for i in range(len(book_data)):
        if book_data['BOOK'][i] == book_name:
            return (book_data.iloc[[i]])
########################################################################
def book_per_person(name,borrow_list):
    book = list()
    book_frame = pd.DataFrame()#columns = ['CODE', 'BOOK', 'AUTHOR']
    for i in range(len(borrow_list)):
        if name == borrow_list.iloc[i,2]:
            book.append(borrow_list.iloc[i,0])
    return book
########################################################################
def return_book_list(borrow_list):
    df = pd.DataFrame()
    available_book = pd.concat([book_data['BOOK'],borrow_list['BOOK']],)
    available_book = available_book.drop_duplicates(keep = False)
    available_book = available_book.values.tolist()
    for i in range(len(available_book)):
        df = pd.concat([df,get_book_info(available_book[i])])
        
    return df
########################################################################
mail = Mailer(email='miukunkun2002@gmail.com',
              password=**)
name = info['STUDENT']
mail = info['Student_Email']
book = book_per_person(name,borrow_list)
text = 'Dear ' ,name, ',' '\nBook borrowed list:',book,'\n Thank you!'
mail.send(receiver= name,  # Email From Any service Provider
          subject='[LIBRAY] Confirmation borrow book',
          message= text)
########################################################################
card = cv2.imread('Student_Card/STUDENT_CARD_00.jpg')
card = cv2.resize(card,(600,400))

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
        if area > 250:
            peri = cv2.arcLength(c,True)
            approx = cv2.approxPolyDP(c,0.02*peri,True)
            # print(len(approx))
            if len(approx) == 4:
                rect_cnts.append(c)   
    rect_cnts = sorted(rect_cnts,key = cv2.contourArea,reverse=True)
    return rect_cnts

def get_conrner_point(c):
    peri = cv2.arcLength(c,True)
    approx = cv2.approxPolyDP(c,0.04*peri,True)
    return approx

def four_points(points):
    points = points.reshape(4,2)
    new_points = np.zeros((4,1,2),dtype="float32")

    s = points.sum(axis = 1)
    new_points[0] = points[np.argmin(s)]
    new_points[3] = points[np.argmax(s)]

    diff = np.diff(points, axis = 1)
    new_points[1] = points[np.argmin(diff)]
    new_points[2] = points[np.argmax(diff)]

    return new_points

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

scan = card_warp[270:370,0:200]
info = student_card_detect(scan)    
print(info)   
cv2.imshow('Scan',scan)
cv2.waitKey(0)