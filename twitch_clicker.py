# coding=utf-8
import pyautogui
from time import strftime
from sys import argv

# Bonus button
BONUS_IM = "bonus.png"
BONUS_COLOR = (0, 245, 154)


'''
Bonus coordinates if one stream in the following pos:
    monitor1
+-----+-------+
|video|another|
+-----+chrome |
|chat |window |
|_□___|_______+
'''

if argv[1] == "1":
    REGIONS = [(63, 1034, 1856, 45)]
else:
    # Coordinates in two stream mode
    REGIONS = [(650, 510, 200, 50), (650, 1034, 200, 45)]

COUNT = 1

while True:
    for R in REGIONS:
        box = pyautogui.locateOnScreen(BONUS_IM, region=R, confidence=0.7)
        print("\r", strftime("%H:%M:%S"), " ", box, sep="", end=" ")
        if box:
            x_cur, y_cur = pyautogui.position()
            pyautogui.click(box)
            pyautogui.moveTo(x_cur, y_cur)
            pyautogui.hotkey('alt', 'tab')
            print(f"Clicked {COUNT}")
            COUNT += 1
        else:
            print("...waiting...", end="")
    del box
    pyautogui.sleep(10)
