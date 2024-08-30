
# cv2.cvtColor takes a numpy ndarray as an argument
import pygame
import numpy as np
from PIL import Image as Img
from tkinter import *
import pytesseract
import time
# importing OpenCV
import cv2
from PIL import ImageGrab
import pyautogui
from pyautogui import press
import pydirectinput
from ctypes import windll, Structure, c_long, byref
import keyboard
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#global variables
havePP = True

#interface
MainWindow = Tk()
MainWindow.title("JuanzinBot")
#MainWindow.configure(background="black")
MainWindow.iconbitmap('favicon-16x16.ico')
MainWindow.geometry("200x200")
MainWindow.resizable(False,False)

AutoFish = IntVar()
start = Label(MainWindow, text="Auto Fish:", fg="black")
start.pack()
autoFishing = Checkbutton(MainWindow, variable=AutoFish)
autoFishing.pack()

StopBotting = IntVar()
Label(MainWindow, text="Stop Bot:", fg="black").pack()
botStopping = Checkbutton(MainWindow, variable=StopBotting)
botStopping.pack()
#hotkeys
keyboard.add_hotkey('home', lambda: StopBot())
keyboard.add_hotkey('delete', lambda: stopAlarm())

pygame.mixer.init()
#functions
def isBattle():
    img = ImageGrab.grab(bbox =(824, 420, 1090, 460))
    custom_oem=r'--oem 3 --psm 4'
    boxName = "get name"
    nameFetched = readBbox(boxName,img) #pytesseract.image_to_string(img,config=custom_oem)
    playerName = "PutzFuiBanidokkk"
    print(nameFetched)
    if nameFetched.find(playerName) == 0:
        print("player found")
        return False
    else:
        print("not player name")
        return True

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

def matching_algo(r, g, b, r_query, g_query, b_query):
    if r == r_query and g == g_query:
        return True
    elif r == r_query and b == b_query:
        return True
    elif b == b_query and g == g_query:
        return  True
    else:
        return False

def autoRune():
    image = ImageGrab.grab()
    mana = image.getpixel((1886, 203))
    blankrune = find_rgb(161, 154, 145)
    maoEsquerda = image.getpixel((1752, 281))
    manaString = str(mana)
    fish = find_rgb(114, 143, 142)
    if "(68, 68, 255)" == manaString:
       print()

def StopBot():
    if AutoFish.get() == 1:
        autoFishing.deselect()
    else:
        autoFishing.select()

def useBerry():
    global havePP
    pyautogui.press('7')
    MainWindow.after(500)
    pyautogui.press('z')
    MainWindow.after(500)
    pyautogui.press('z')
    MainWindow.after(500)
    pyautogui.press('z')
    havePP = True

def runAway():
    bagbox = ImageGrab.grab(bbox =(883, 692, 970, 731))
    custom_oem=r'--oem 3 --psm 4'
    bag = pytesseract.image_to_string(bagbox,config=custom_oem)
    if bag.find("RUN") == 0:
        #pyautogui.click(x=550, y=684, button='left', clicks=3, interval=0.25)
        pydirectinput.press(['down', 'right']) #this is the updated line of code
        pyautogui.press("z")

def isHorde():
    hordebox = ImageGrab.grab(bbox =(246, 178, 1639, 339))
    
    horde = readBbox("check horde", hordebox) #pytesseract.image_to_string(hordebox,config=custom_oem)
    mob = str(horde).split(" ")
    smeargles = []
    print(smeargles)
    for smeargle in mob:
        if smeargle == "Smeargle":
            smeargles.append(smeargle)
    if len(smeargles) > 1:
        return True
    return False

def bfs(visited, queue, array, node):
    # I make BFS itterative instead of recursive
    def getNeighboor(array, node):
        neighboors = []
        if node[0]+1<array.shape[0]:
            if array[node[0]+1,node[1]] == 0:
                neighboors.append((node[0]+1,node[1]))
        if node[0]-1>0:
            if array[node[0]-1,node[1]] == 0:
                neighboors.append((node[0]-1,node[1]))
        if node[1]+1<array.shape[1]:
            if array[node[0],node[1]+1] == 0:
                neighboors.append((node[0],node[1]+1))
        if node[1]-1>0:
            if array[node[0],node[1]-1] == 0:
                neighboors.append((node[0],node[1]-1))
        return neighboors

    queue.append(node)
    visited.add(node)

    while queue:
        current_node = queue.pop(0)
        for neighboor in getNeighboor(array, current_node):
            if neighboor not in visited:
    #             print(neighboor)
                visited.add(neighboor)
                queue.append(neighboor)

def removeIsland(img_arr, threshold):
    # !important: the black pixel is 0 and white pixel is 1
    while 0 in img_arr:
        x,y = np.where(img_arr == 0)
        point = (x[0],y[0])
        visited = set()
        queue = []
        bfs(visited, queue, img_arr, point)
        
        if len(visited) <= threshold:
            for i in visited:
                img_arr[i[0],i[1]] = 1
        else:
            # if the cluster is larger than threshold (i.e is the text), 
            # we convert it to a temporary value of 2 to mark that we 
            # have visited it. 
            for i in visited:
                img_arr[i[0],i[1]] = 2
                
    img_arr = np.where(img_arr==2, 0, img_arr)
    return img_arr

def readBbox(name, bbox):
   # captchabox = ImageGrab.grab(bbox =(522, 542, 1104, 734))
    # Convert to grayscale
    c_gray = cv2.cvtColor(np.array(bbox), cv2.COLOR_RGB2GRAY)
    # Median filter
    #out = cv2.medianBlur(c_gray,3)
    #cv2.imshow(name,out)
    #cv2.waitKey(0)
    custom_oem=r'--oem 3 --psm 4'
    print(pytesseract.image_to_string(c_gray,config=custom_oem))
    return pytesseract.image_to_string(c_gray,config=custom_oem)
    #mob = str(horde).split(" ")

def alertCaptcha():
    captchabox = ImageGrab.grab(bbox =(322, 124, 1468, 360))
    captcha = readBbox("captcha", captchabox)
    print(captcha)
    print(captcha.find("CAPTCHA"))
    try:
        getCaptcha = captcha.split("\n")
        print("captcha: ",getCaptcha[1])

        if "CAPTCHA" in getCaptcha[1]:
            print("play alarm")
            playAlarm()
            return True
    except:
        pass
    return False

def playAlarm():
    pygame.mixer.music.load("alarm.mp3")
    pygame.mixer.music.play(loops=-1)

def stopAlarm():
    pygame.mixer.music.stop()

def Startbot():
    if AutoFish.get() == 1:
        global havePP
        custom_oem=r'--oem 3 --psm 4'
        if not alertCaptcha():
            if isBattle():
                alertCaptcha()
                if isHorde():
                    runAway()
                else:
                    fightbox = ImageGrab.grab(bbox =(456, 588, 562, 623))
                    boxName = "fight box"
                    fight = readBbox(boxName,fightbox) #pytesseract.image_to_string(fightbox,config=custom_oem)
                    if havePP:
                        pydirectinput.press(['down'])
                        if fight.find("FIGHT") == 0:
                            pyautogui.click(x=500, y=600, button='left', clicks=3, interval=0.25)
                        noPPbox = ImageGrab.grab(bbox =(297, 565, 823, 661))
                        boxName = "no pp"
                        noPP = readBbox(boxName, noPPbox) #pytesseract.image_to_string(noPPbox,config=custom_oem)
                        noPPSplit = noPP.split('\n')
                        #print(noPPSplit)
                        for sentence in noPPSplit:
                            if 'But' and 'there' in sentence:
                                print("no PP left")
                                havePP = False
                    else:
                        runAway()
                        MainWindow.after(4000, useBerry)

                    cancelLearnMoveBox = ImageGrab.grab(bbox =(852, 684, 942, 703))
                    custom_oem=r'--oem 3 --psm 4'
                    boxName = "cancel Move"
                    cancelLearn = readBbox(boxName,cancelLearnMoveBox) #pytesseract.image_to_string(cancelLearnMoveBox,config=custom_oem)
                    cancelsplit = cancelLearn.split(" ")
                    try:
                        if cancelsplit[1].find("Cancel") == 0:
                            pyautogui.click(x=860, y=690, button='left')
                            pyautogui.press("z")
                    except:
                        pass
            else:
                if havePP:
                    pydirectinput.press(['up', 'up', 'up', 'up', 'up', 'up']) #this is the updated line of code
                    pydirectinput.press(['down', 'down', 'down', 'down', 'down', 'down']) #this is the updated line of code
        else:
            StopBot()
        
    if StopBotting.get() == 1:
        autoFishing.deselect()
        botStopping.deselect()
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


#time.sleep(2)
#pos = queryMousePosition()
#
##print(pos)
#position = x,y = pos[0],pos[1]
#image = ImageGrab.grab()
#aa = image.getpixel(position)
##print(aa)