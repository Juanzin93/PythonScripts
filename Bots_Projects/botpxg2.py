import pyautogui
import time
import keyboard
import pygame
import threading

def playAlarm():
    pygame.mixer.music.load("alarm.mp3")
    pygame.mixer.music.play(loops=-1)

def stopAlarm():
    pygame.mixer.music.stop()

pygame.mixer.init()
keyboard.add_hotkey('delete', lambda: stopAlarm())
firstWave = True
secondWave = True
def pegaLootTacaBall():
    try:
        deadlapras = pyautogui.locateOnScreen("lapras.png", confidence=0.75)
        lapras_x, lapras_y = pyautogui.center(deadlapras)
        pyautogui.moveTo(lapras_x, lapras_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
    except:
        pass
    try:
        deadlapras = pyautogui.locateOnScreen("lapras.png", confidence=0.75)
        lapras_x, lapras_y = pyautogui.center(deadlapras)
        pyautogui.moveTo(lapras_x, lapras_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
    except:
        pass
    try:
        deadwalrein = pyautogui.locateOnScreen("walrein.png", confidence=0.75)
        walrein_x, walrein_y = pyautogui.center(deadwalrein)
        pyautogui.moveTo(walrein_x, walrein_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
    except:
        pass
    try:
        deadwalrein = pyautogui.locateOnScreen("walrein.png", confidence=0.75)
        walrein_x, walrein_y = pyautogui.center(deadwalrein)
        pyautogui.moveTo(walrein_x, walrein_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
    except:
        pass
    try:
        deadgya = pyautogui.locateOnScreen("gya.png", confidence=0.75)
        gya_x, gya_y = pyautogui.center(deadgya)
        pyautogui.moveTo(gya_x, gya_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
    except:
        pass
    try:
        deadgya = pyautogui.locateOnScreen("gya.png", confidence=0.75)
        gya_x, gya_y = pyautogui.center(deadgya)
        pyautogui.moveTo(gya_x, gya_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
    except:
        pass
    try:
        deadmantine = pyautogui.locateOnScreen("mantine.png", confidence=0.75)
        mantine_x, mantine_y = pyautogui.center(deadmantine)
        pyautogui.moveTo(mantine_x, mantine_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
        
    except:
        pass
    try:
        deadmantine = pyautogui.locateOnScreen("mantine.png", confidence=0.75)
        mantine_x, mantine_y = pyautogui.center(deadmantine)
        pyautogui.moveTo(mantine_x, mantine_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
        
    except:
        pass
    try:
        deadkingdra = pyautogui.locateOnScreen("kingdra.png", confidence=0.75)
        kingdra_x, kingdra_y = pyautogui.center(deadkingdra)
        pyautogui.moveTo(kingdra_x, kingdra_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
    except:
        pass
    try:
        deadkingdra = pyautogui.locateOnScreen("kingdra.png", confidence=0.75)
        kingdra_x, kingdra_y = pyautogui.center(deadkingdra)
        pyautogui.moveTo(kingdra_x, kingdra_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
    except:
        pass
    
    try:
        deadtentacruel = pyautogui.locateOnScreen("tentacruel.png", confidence=0.75)
        tentacruel_x, tentacruel_y = pyautogui.center(deadtentacruel)
        pyautogui.moveTo(tentacruel_x, tentacruel_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
    except:
        pass
    
    try:
        deadtentacruel = pyautogui.locateOnScreen("tentacruel.png", confidence=0.75)
        tentacruel_x, tentacruel_y = pyautogui.center(deadtentacruel)
        pyautogui.moveTo(tentacruel_x, tentacruel_y)
        pyautogui.click(button='right')
        pyautogui.click(button='middle')
    except:
        pass
        
while True:
    thread = threading.Thread(target=pegaLootTacaBall)
    thread.start()
        
    bolhas = pyautogui.locateOnScreen("bolhas.png", confidence=0.75)    
    print(bolhas)
    if bolhas != None:
        
        fishingrod = pyautogui.locateOnScreen("fishingrod.png", confidence=0.6)
        fishingrod_x, fishingrod_y = pyautogui.center(fishingrod)
        pyautogui.moveTo(fishingrod_x,fishingrod_y)
        pyautogui.click()
        time.sleep(1)
        antibot = pyautogui.locateOnScreen("antibot.png", confidence=0.75)
        if antibot:
            playAlarm()
            time.sleep(20)
        #try:
        #    atk = pyautogui.locateOnScreen("atk2.png")
        #    atk_x, atk_y = pyautogui.center(atk)
        #    pyautogui.moveTo(atk_x, atk_y)
        #    pyautogui.click()
        #    time.sleep(1)
        #    atk2 = pyautogui.locateOnScreen("atk3.png")
        #    atk2_x, atk2_y = pyautogui.center(atk2)
        #    pyautogui.moveTo(atk2_x, atk2_y)
        #    pyautogui.click()
        #    time.sleep(1)
        #except:
        #    try:
        #        atk = pyautogui.locateOnScreen("atk1.png")
        #        atk_x, atk_y = pyautogui.center(atk)
        #        pyautogui.moveTo(atk_x, atk_y)
        #        pyautogui.click()
        #        time.sleep(1)
        #        atk2 = pyautogui.locateOnScreen("atk4.png")
        #        atk2_x, atk2_y = pyautogui.center(atk2)
        #        pyautogui.moveTo(atk2_x, atk2_y)
        #        pyautogui.click()
        #        time.sleep(1)
        #    except:
        if firstWave:
            keyboard.press_and_release('f4')
            time.sleep(0.5)
            keyboard.press_and_release('f6')
            firstWave = False
            secondWave = True
        elif secondWave:
            keyboard.press_and_release('f5')
            time.sleep(0.5)
            keyboard.press_and_release('f7')
            firstWave = True
            secondWave = False
        
        bolhas_x, bolhas_y = pyautogui.center(bolhas)
        
        pyautogui.moveTo(fishingrod_x,fishingrod_y)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.moveTo(bolhas_x, bolhas_y)
        time.sleep(0.5)

        pyautogui.click()
    