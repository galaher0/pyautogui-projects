# coding=utf-8
import pyautogui
from time import strftime
from sys import argv


# Bonus button
BONUS_IM = "bonus.png"

if argv[1] == "1":
    '''Bonus coordinates if one stream in the following pos:
    +-----+
    |video|
    +-----+
    |chat |
    |_□___|
    '''
    REGIONS = [(63, 1034, 1856, 33)]
else:
    # Coordinates in two stream mode
    REGIONS = [(650, 510, 200, 50), (650, 1034, 200, 33)]

COUNT = 1

while True:
    for R in REGIONS:
        box = pyautogui.locateOnScreen(BONUS_IM, region=R)
        print("\r", strftime("%H:%M:%S"), " ", box, sep="", end=" ")
        if box:
            x_cur, y_cur = pyautogui.position()
            place_to_click = pyautogui.center(box)
            pyautogui.click(place_to_click)
            print(f"Clicked {COUNT}")
            COUNT += 1
            pyautogui.moveTo(x_cur, y_cur)
#            pyautogui.sleep(20)
        else:
            print("...waiting...", end="")
    pyautogui.sleep(10)
