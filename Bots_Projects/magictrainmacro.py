import pyautogui
import keyboard
running = True
def toggleFunction():
    global running
    if running:
        running = False
    else:
        running = True

keyboard.add_hotkey('home', toggleFunction)
while running:
    pyautogui.click(x=1756, y=654, button='right',clicks=2, interval=1)
    pyautogui.press('f1')