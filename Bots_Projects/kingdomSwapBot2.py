
# cv2.cvtColor takes a numpy ndarray as an argument
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
from ctypes import windll, Structure, c_long, byref
import keyboard


MainWindow = Tk()
MainWindow.title("JuanzinBot")
#MainWindow.configure(background="black")
#MainWindow.iconbitmap('favicon-16x16.ico')
MainWindow.geometry("200x200")
MainWindow.resizable(False,False)

AutoFish = IntVar()
start = Label(MainWindow, text="Auto Fish:", fg="black")
start.pack()
autoFishing = Checkbutton(MainWindow, variable=AutoFish)
autoFishing.pack()

AutoHeal = IntVar()
Label(MainWindow, text="Auto Heal:", fg="black").pack()
autoHealing = Checkbutton(MainWindow, variable=AutoHeal)
autoHealing.pack()

AutoRune = IntVar()
Label(MainWindow, text="Auto Rune:", fg="black").pack()
autoRuning = Checkbutton(MainWindow, variable=AutoRune)
autoRuning.pack()
StopBotting = IntVar()
Label(MainWindow, text="Stop Bot:", fg="black").pack()
botStopping = Checkbutton(MainWindow, variable=StopBotting)
botStopping.pack()
StartFishing = False

def find_rgb(r_query, g_query, b_query):
            img = ImageGrab.grab()
            pix = img.load()
            coordinates= []
            for x in range(img.size[0]):
                for y in range(img.size[1]):
                    r, g, b = pix[x,y]
                    if matching_algo(r, g, b, r_query, g_query, b_query):
                        #print("{},{} contains {}-{}-{} ".format(x, y, r, g, b))
                        if r_query == r and g_query == g and b_query == b:
                            return x,y
                            coordinates.append((x, y))
            #return(coordinates)

def matching_algo(r, g, b, r_query, g_query, b_query):
    if r == r_query and g == g_query:
        return True
    elif r == r_query and b == b_query:
        return True
    elif b == b_query and g == g_query:
        return  True
    else:
        return False

def fishing():
    fishingRod = find_rgb(155, 106, 64)
    pyautogui.moveTo(fishingRod)
    start.after(100)

    pyautogui.click(button='right')
    water = find_rgb(0, 5, 159)
    clearWater = find_rgb(0, 5, 159)
    if water != None:
        pyautogui.moveTo(water)
        start.after(100)

        pyautogui.click(button='left')
    elif clearWater != None:
        pyautogui.moveTo(clearWater)
        start.after(100)

        pyautogui.click(button='left')

#blankrune = find_rgb(161, 154, 145)
#print(blankrune)
def autoRune():
    image = ImageGrab.grab()
    mana = image.getpixel((1886, 203))
    blankrune = find_rgb(161, 154, 145)
    maoEsquerda = image.getpixel((1752, 281))
    manaString = str(mana)
    fish = find_rgb(114, 143, 142)
    if "(68, 68, 255)" == manaString:
        if StartFishing == True and AutoFish.get() == 1:
            autoFishing.deselect()
        #
        #if blankrune != None:
        #    if str(maoEsquerda) == "(158, 152, 145)":
            pyautogui.press('f7')
        #        start.after(500)
        #        pyautogui.moveTo(blankrune)
        #        pyautogui.dragTo(1746, 284, 1.5, button='left')
            pyautogui.moveTo(fish)
            pyautogui.click(button='right', clicks=4, interval=0.25)
            if StartFishing == True:
                autoFishing.select()
#
        #if blankrune == None:
        #    StopBot()

def exuraHeal():
    image = ImageGrab.grab()
    health = image.getpixel((1022, 733))
    healthString = str(health)
    if "(237, 77, 29)" != healthString:
        #pyautogui.press('f2')
        pyautogui.click(button='left')




def StopBot():
    if StopBotting.get() == 1:
        botStopping.deselect()
    else:
        botStopping.select()
keyboard.add_hotkey('home', lambda: StopBot())
def Startbot():
    if AutoHeal.get() == 1:
        exuraHeal()
    if AutoRune.get() == 1:
        autoRune()
    if AutoFish.get() == 1:
        global StartFishing
        if StartFishing == False:
            StartFishing = True
        fishing()
    
    if StopBotting.get() == 1:
        autoHealing.deselect()
        autoRuning.deselect()
        autoFishing.deselect()
        botStopping.deselect()
        StartFishing = False
    start.after(100, Startbot)

Startbot()
MainWindow.mainloop()
#class POINT(Structure):
#    _fields_ = [("x", c_long), ("y", c_long)]
#def queryMousePosition():
#    pt = POINT()
#    cordinate = []
#    windll.user32.GetCursorPos(byref(pt))
#    cordinate.append(pt.x)
#    cordinate.append(pt.y)
#    return cordinate
#
#
#time.sleep(2)
#pos = queryMousePosition()
#
##print(pos)
#position = x,y = pos[0],pos[1]
#image = ImageGrab.grab()
#aa = image.getpixel(position)
##print(aa)

        
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