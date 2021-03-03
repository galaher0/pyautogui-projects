# coding=utf-8

import pyautogui
from time import strftime


TAB = "b_tab.png"
TAB2 = "b_tab_dark.png"
TAB3 = "b_tab3.png"
CAPTCHA = "captcha.png"
CAPTCHA_APPR = "captcha_appr.png"
ROLL_BTN = "roll_btn.png"

TAB_REGION = (674, 17, 1000, 20)
CAPTCHA_REGION = (1126, 785, 674, 90)
ROLL_REGION = (1200, 870, 600, 80)

PIXELS_TO_GO_DOWN = 450

CLICKS_TO_SCROLL = -10

COUNT = 1

# outer cycle, repeating process of click
while True:
    # waiting for tab to finish countdown
    while True:
        tab_box = pyautogui.locateOnScreen(TAB, region=TAB_REGION) or \
        pyautogui.locateOnScreen(TAB2, region=TAB_REGION) or \
        pyautogui.locateOnScreen(TAB3, region=TAB_REGION)
        print(f'\r{strftime("%H:%M:%S")}', end=" ")

        # launching the process of manipulating the page
        if tab_box:
            print("Tab found...", end=" ")
            tab_coord_to_click = pyautogui.center(tab_box)

            x_cur, y_cur = pyautogui.position() # saving mouse position

            pyautogui.click(tab_coord_to_click)
            print("and clicked.", end=" ")
            pyautogui.sleep(0.01)

            # ensuring scroll to bottom (in order to regions to work)
            # and then clicking captcha and roll button
            while True:
                pyautogui.scroll(CLICKS_TO_SCROLL, tab_coord_to_click[0], PIXELS_TO_GO_DOWN)
                pyautogui.sleep(0.2)

                captcha_box = pyautogui.locateOnScreen(CAPTCHA, region=CAPTCHA_REGION)
                if captcha_box:
                    print(f"Captcha found...", end=" ")
                    robot_coord_to_click = pyautogui.center(captcha_box)
                    pyautogui.click(robot_coord_to_click)
                    print("and clicked.", end=" ")
                    pyautogui.sleep(0.2)

                    # waiting for captcha approvement and then clicking ROLL
                    captcha_timer = 0
                    captcha_timer_limit = 100 # 20 sec
                    wait_for_captcha_sec = 0.2
                    while True:
                        if captcha_timer < captcha_timer_limit:
                            if pyautogui.locateOnScreen(CAPTCHA_APPR, region=CAPTCHA_REGION):

                                print(f"Captcha ok, time limit: "
                                f"{captcha_timer * wait_for_captcha_sec}/"
                                f"{captcha_timer_limit * wait_for_captcha_sec}.", end=" ")

                                # clicking roll btn after captcha approvement
                                roll_box = pyautogui.locateOnScreen(ROLL_BTN, region=ROLL_REGION)
                                if roll_box:
                                    print("Roll btn found.", end=" ")
                                    roll_coord_to_click = pyautogui.center(roll_box)
                                    pyautogui.click(roll_coord_to_click)
                                    print(f"Clicked {COUNT}.") # the end of page manipulation
                                    COUNT += 1

                                    # waiting for an hour in the successful loop
                                    pyautogui.moveTo(x_cur, y_cur)
                                    pyautogui.sleep(60*60) # main cycle, successful inner loop, waiting for countdown
                                    break # from captcha loop
                                else:
                                    print("Roll btn not found")
                                    break # from captcha loop
                            captcha_timer += 1
                            pyautogui.sleep(wait_for_captcha_sec)
                        else:
                            print("Captcha time limit exceeded") # the end of page manipulation
                            break # from captcha loop
                    break # from scroll loop
                else:
                    print("...scrolling...", end=" ")
                    pyautogui.sleep(0.5)
                # next scroll loop
            break # end of page manipulation (either successful or not)
        else:
            pyautogui.sleep(5) # inner loop waiting for page to load


