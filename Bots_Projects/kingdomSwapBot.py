
# cv2.cvtColor takes a numpy ndarray as an argument
import numpy as nm
from PIL import Image
from tkinter import *
import time
#import OpenCV
import cv2
from PIL import ImageGrab
import pyautogui
from pyautogui import press
from ctypes import windll, Structure, c_long, byref
import keyboard
import itertools

MainWindow = Tk()
MainWindow.title("JuanzinBot")
#MainWindow.configure(background="black")
#MainWindow.iconbitmap('favicon-16x16.ico')
MainWindow.geometry("400x400")
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

ManaPerceLabel = Label(MainWindow, text="Mana %:", fg="black")
ManaPerceLabel.place(x=10, y=30)
manaPerce = Entry(MainWindow, width=5)
manaPerce.place(x=60, y=30)

AutoRune = IntVar()
autoRuningLabel = Label(MainWindow, text="Auto Rune:", fg="black")
autoRuningLabel.place(x=50, y=10)
autoRuning = Checkbutton(MainWindow, variable=AutoRune)
autoRuning.place(x=100, y=30)
StopBotting = IntVar()
Label(MainWindow, text="Stop Bot:", fg="black").pack()
botStopping = Checkbutton(MainWindow, variable=StopBotting)
botStopping.pack()
StartFishing = False

class LeftHandBoxWidget(object):
    def getScreenshot(self):
        image = ImageGrab.grab()
        image.save('1.jpg')
        self.original_image = cv2.imread('1.jpg')
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points
        self.leftHand_coordinates = []

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.leftHand_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse button release
        elif event == cv2.EVENT_LBUTTONUP:
            self.leftHand_coordinates.append((x,y))
            print('top left: {}, bottom right: {}'.format(self.leftHand_coordinates[0], self.leftHand_coordinates[1]))
            print('x,y,w,h : ({}, {}, {}, {})'.format(self.leftHand_coordinates[0][0], self.leftHand_coordinates[0][1], self.leftHand_coordinates[1][0] - self.leftHand_coordinates[0][0], self.leftHand_coordinates[1][1] - self.leftHand_coordinates[0][1]))

            # Draw rectangle 
            cv2.rectangle(self.clone, self.leftHand_coordinates[0], self.leftHand_coordinates[1], (36,255,12), 2)
            cv2.imshow("image", self.clone) 

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        LeftHandBoxWidget.getScreenshot(self)
        return self.clone

def getLeftHandBox():
    boundingbox_widget = LeftHandBoxWidget()
    cv2.imshow('image', boundingbox_widget.show_image())
    key = cv2.waitKey(1)
    #start.after(100, getPixelBox)
    # Close program with keyboard 'q'
    if key == ord('q'):
        cv2.destroyAllWindows()
        exit(1)

class HealthBoxWidget(object):
    def getScreenshot(self):
        image = ImageGrab.grab()
        image.save('1.jpg')
        self.original_image = cv2.imread('1.jpg')
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points
        self.health_coordinates = []

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.health_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse button release
        elif event == cv2.EVENT_LBUTTONUP:
            self.health_coordinates.append((x,y))
            print('top left: {}, bottom right: {}'.format(self.health_coordinates[0], self.health_coordinates[1]))
            print('x,y,w,h : ({}, {}, {}, {})'.format(self.health_coordinates[0][0], self.health_coordinates[0][1], self.health_coordinates[1][0] - self.health_coordinates[0][0], self.health_coordinates[1][1] - self.health_coordinates[0][1]))

            # Draw rectangle 
            cv2.rectangle(self.clone, self.health_coordinates[0], self.health_coordinates[1], (36,255,12), 2)
            cv2.imshow("image", self.clone) 

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        HealthBoxWidget.getScreenshot(self)
        return self.clone

def getHealthBox():
    boundingbox_widget = HealthBoxWidget()
    cv2.imshow('image', boundingbox_widget.show_image())
    key = cv2.waitKey(1)
    #start.after(100, getPixelBox)
    # Close program with keyboard 'q'
    if key == ord('q'):
        cv2.destroyAllWindows()
        exit(1)

mana_coordinates = []

class ManaBoxWidget(object):
    def getScreenshot(self):
        image = ImageGrab.grab()
        image.save('1.jpg')
        self.original_image = cv2.imread('1.jpg')
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points
    
    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            global mana_coordinates
            mana_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse button release
        elif event == cv2.EVENT_LBUTTONUP:
            mana_coordinates.append((x,y))
            print('top left: {}, bottom right: {}'.format(mana_coordinates[0], mana_coordinates[1]))
            print('x,y,w,h : ({}, {}, {}, {})'.format(mana_coordinates[0][0], mana_coordinates[0][1], mana_coordinates[1][0] - mana_coordinates[0][0], mana_coordinates[1][1] - mana_coordinates[0][1]))

            # Draw rectangle 
            cv2.rectangle(self.clone, mana_coordinates[0], mana_coordinates[1], (36,255,12), 2)
            cv2.imshow("image", self.clone) 

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        ManaBoxWidget.getScreenshot(self)
        return self.clone

def getManaBox():
    boundingbox_widget = ManaBoxWidget()
    cv2.imshow('image', boundingbox_widget.show_image())
    key = cv2.waitKey(1)
    #start.after(100, getPixelBox)
    # Close program with keyboard 'q'
    if key == ord('q'):
        cv2.destroyAllWindows()
        exit(1)

water_coordinates = []

class WaterBoxWidget(object):
    def getScreenshot(self):
        image = ImageGrab.grab()
        image.save('1.jpg')
        self.original_image = cv2.imread('1.jpg')
        self.clone = self.original_image.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.extract_coordinates)

        # Bounding box reference points
    
    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            global water_coordinates
            water_coordinates = [(x,y)]

        # Record ending (x,y) coordintes on left mouse button release
        elif event == cv2.EVENT_LBUTTONUP:
            water_coordinates.append((x,y))
            print('top left: {}, bottom right: {}'.format(water_coordinates[0], water_coordinates[1]))
            print('x,y,w,h : ({}, {}, {}, {})'.format(water_coordinates[0][0], water_coordinates[0][1], water_coordinates[1][0] - water_coordinates[0][0], water_coordinates[1][1] - water_coordinates[0][1]))

            # Draw rectangle 
            cv2.rectangle(self.clone, water_coordinates[0], water_coordinates[1], (36,255,12), 2)
            cv2.imshow("image", self.clone) 

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.original_image.copy()

    def show_image(self):
        ManaBoxWidget.getScreenshot(self)
        return self.clone

def getWaterBox():
    boundingbox_widget = WaterBoxWidget()
    cv2.imshow('image', boundingbox_widget.show_image())
    key = cv2.waitKey(1)
    #start.after(100, getPixelBox)
    # Close program with keyboard 'q'
    if key == ord('q'):
        cv2.destroyAllWindows()
        exit(1)


LeftHandBox = Button(text="Find Left Hand", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=getLeftHandBox)
LeftHandBox.pack()

HealthBox = Button(text="Find Health", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=getHealthBox)
HealthBox.pack()

ManaBox = Button(text="Find Mana", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=getManaBox)
ManaBox.pack()

ManaBox = Button(text="Find Water", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=getWaterBox)
ManaBox.pack()

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
    water_x1 = (water_coordinates[0][0])
    water_y1 = (water_coordinates[0][1])
    water_x2 = (water_coordinates[1][0])
    water_y2 = (water_coordinates[1][1])
    insideWaterBoxX = water_x2 - water_x1
    insideWaterBoxY = water_y2 - water_y1
    middleOfWaterBoxY = insideWaterBoxY / 2
    middleOfWaterBoxX = insideWaterBoxX / 2
    image = ImageGrab.grab()
    fishingRod = find_rgb(155, 106, 64)
    pyautogui.moveTo(fishingRod)
    pyautogui.click(button='right')
    #water = find_rgb(17, 38, 167)
    water1 = water_x1 + middleOfWaterBoxX, water_y1 + middleOfWaterBoxY
    waterPixel = image.getpixel(water1)
    print(waterPixel)

    water = find_rgb(15, 37, 161)

    print(waterPixel)
    clearWater = find_rgb(34, 136, 169)
    if water != None:
        pyautogui.moveTo(water)
        pyautogui.click(button='left')
    elif clearWater != None:
        pyautogui.moveTo(clearWater)
        pyautogui.click(button='left')

#blankrune = find_rgb(161, 154, 145)
#print(blankrune)

def autoRune():
    mana_x1 = (mana_coordinates[0][0])
    mana_y1 = (mana_coordinates[0][1])
    mana_x2 = (mana_coordinates[1][0])
    mana_y2 = (mana_coordinates[1][1])
    image = ImageGrab.grab()

    input = [(mana_x1, mana_y1), (mana_x2, mana_y2)]
    x_coords = [x for x in range(input[0][0], input[1][0] + 1)]
    y_coords = [y for y in range(input[0][1], input[1][1] + 1)]
    output = list(itertools.product(x_coords, y_coords))
    insideManaBoxX = mana_x2 - mana_x1
    insideManaBoxY = mana_y2 - mana_y1
    middleOfManaBoxY = insideManaBoxY / 2
    #print(insideManaBoxX)
    manaPercent = insideManaBoxX / 100
    manaSevenFivePercent = round(manaPercent * int(manaPerce.get())) # get mana percent textentry
    #print(manaSevenFivePercent)

    #for i in range(len(output)):
    #    if str(image.getpixel(output[i])) == "(158, 152, 145)":
    #        print(i)
    manaMidPos = (mana_y1 + middleOfManaBoxY)
    manaLightHeal = mana_x1 + manaSevenFivePercent
    mana = image.getpixel((manaLightHeal, manaMidPos))
    print(f"mana is {mana}")
    blankrune = find_rgb(161, 154, 145)
    maoEsquerda = ImageGrab.grab(bbox=(1739, 84, 1762, 104))
    maoEsquerdaPixel = maoEsquerda.getpixel((15, 15))
    manaString = str(mana)
    fish = find_rgb(114, 143, 142)
    if "(68, 68, 255)" == manaString:
        if StartFishing == True and AutoFish.get() == 1:
            autoFishing.deselect()
        
        if blankrune != None:
            if str(maoEsquerdaPixel) == "(158, 152, 145)":
                pyautogui.press('f7')
                start.after(500)
                pyautogui.moveTo(blankrune)
                pyautogui.dragTo(1746, 284, 1.5, button='left')
                pyautogui.moveTo(fish)
                pyautogui.click(button='right', clicks=4, interval=0.25)
                if StartFishing == True:
                    autoFishing.select()

        if blankrune == None:
            StopBot()

def exuraHeal():
    image = ImageGrab.grab()
    health = image.getpixel((1097, 687))
    healthString = str(health)
    print(health)
    pos = find_rgb(245, 80, 31)
    if "(245, 80, 31)" == healthString or "(237, 77, 29)" == healthString:
        #pyautogui.press('f2')
        print("clicked")
        pyautogui.moveTo(pos)
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
#position = x,y = pos[0],pos[1]
#image = ImageGrab.grab()
#aa = image.getpixel(position)
#print(aa)

        
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