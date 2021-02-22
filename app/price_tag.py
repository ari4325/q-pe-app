import cv2
import numpy as np
import urllib
import PIL
from flask import Flask, request, Response
import base64
from PIL import Image
import os , io , sys
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C://Program Files/Tesseract-OCR/tesseract'

def processImg(img):
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    blue_lower = np.array([110,50,50], np.uint8) 
    blue_upper = np.array([130,255,255], np.uint8) 
    blue_mask = cv2.inRange(hsv_image, blue_lower, blue_upper) 

    kernel = np.ones((5,5), "uint8")
    blue_mask = cv2.dilate(blue_mask, kernel) 
    res_blue = cv2.bitwise_and(img, img, 
                                mask = blue_mask) 

    contours, hierarchy = cv2.findContours(blue_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE) 

    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour)  
        '''cv2.drawContours(img, contour, -1, (255, 0, 255), 1)
        print(area)
        img = cv2.rectangle(img, (x, y),  
                                    (x + w, y + h),  
                                    (20, 100, 255), 2) 
            
        cv2.putText(img, "MRP", (x, y), 
                    cv2.FONT_ITALIC, 0.8, 
                    (0, 0, 255))  '''   
        x, y, w, h = cv2.boundingRect(contour) 
        return img[y:y+h, x:x+w]


app = Flask(__name__)
@app.route('/upload', methods = ['POST'])
def upload():
    img = cv2.imdecode(np.fromstring(request.files['image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)
    img_processed = processImg(img)
    '''img = Image.fromarray(img.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())'''
    img = Image.fromarray(img_processed.astype("uint8"))
    text = pytesseract.image_to_string(img)
    text = ''.join(filter(str.isdigit, text))
    return Response(response=text, status=200, mimetype="application/json")


@app.route('/')
def default():
    return "Welcome to QPe"