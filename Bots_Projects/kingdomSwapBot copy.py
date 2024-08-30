
# cv2.cvtColor takes a numpy ndarray as an argument
import ctypes
import numpy as nm
from PIL import Image
from tkinter import *
import pytesseract
import time
# importing OpenCV
import cv2
from PIL import ImageGrab
import pyautogui
from pyautogui import press
from ctypes import c_uint64, windll, Structure, c_long, byref
#from process_interface import ProcessInterface

#def main():
#process = ProcessInterface()
#process.open('KingdomSwapDX.exe')
#base_address = 0x100000000
#step8_pointer_address = 0x944DD0
#print(bytearray.fromhex("33 31 37 38 33"))
#step8_static_address = c_uint64(base_address + step8_pointer_address)
#print(str(step8_static_address).encode('utf-8'))
#step8_base_pointer_val = c_uint64.from_buffer(process.read_memory(step8_static_address, buffer_size=8)).value
#print(step8_base_pointer_val)
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]



def queryMousePosition():
    pt = POINT()
    cordinate = []
    windll.user32.GetCursorPos(byref(pt))
    cordinate.append(pt.x)
    cordinate.append(pt.y)
    return cordinate

time.sleep(2)
pos = queryMousePosition()

print(pos)
position = x,y = pos[0],pos[1]
image = ImageGrab.grab()
aa = image.getpixel(position)
print(aa)

        
#def imToString():
# 
#   # Path of tesseract executable
#   pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#   while(True):
# 
#       # ImageGrab-To capture the screen image in a loop. 
#       # Bbox used to capture a specific area.
#       #grabhealth = ImageGrab.grab(bbox =(1786, 167, 1849, 200))
#       #grabmana = ImageGrab.grab(bbox =(1729, 197, 1900, 209))
#       #cordinates = x, y = 1864, 206
#       #pixel = grabmana.getpixel(cordinates)
#       image = ImageGrab.grab()
#       health = image.getpixel((1784, 184))
#       mana = image.getpixel((1886, 203))
#       blankrune = image.getpixel((1847, 555))
#       healthString = str(health)
#       manaString = str(mana)
#       blankString = str(blankrune)
#       
#       #print(blankrune)
#       if "(255, 68, 68)" != healthString:
#           pyautogui.press('f2')
#
#       if "(68, 68, 255)" == manaString:
#           pyautogui.press('f7')
#           if "(161, 154, 145)" == blankString:
#               pyautogui.moveTo(1847, 555)
#               pyautogui.dragTo(1746, 284, 1, button='left')
#               pyautogui.click(x=1824, y=318, button='right', clicks=3, interval=0.25)
#
            #gethealth = cv2.cvtColor(nm.array(grabhealth), cv2.COLOR_BGR2GRAY)
            #getmana = cv2.cvtColor(nm.array(grabmana), cv2.COLOR_BGR2GRAY)
            #cv2.dilate(getmana, (5, 5), getmana)
            #cv2.dilate(gethealth, (5, 5), gethealth)
            #print(pytesseract.image_to_string(gethealth))
            #print(pytesseract.image_to_string(getmana))
            #custom_oem=r'digits --oem 1 --psm 7 -c tessedit_char_whitelist=0123456789/'
            #health = pytesseract.image_to_string(gethealth, config=custom_oem)
            #mana = pytesseract.image_to_string(getmana, config=custom_oem)

            #splitHealth = health.split()
            #splitMana = mana.split("/")
            ##splitMaxMana = splitMana[1].split("#")
            #print(splitMana)
            #print(splitMana[0])
            #print(splitMaxMana[1])
            #if int(splitHealth[0]) <= 190:
            #    pyautogui.press('f2')
            #else:
            #    print("false")
            #    
            #if int(splitMana[0]) >= 250:
            #    pyautogui.press('f7')
            #else:
            #    print("false")
  
# Calling the function
#imToString()