# coding=utf-8

import pyautogui
from time import strftime
from pyscreeze import Box
from typing import Tuple


# CONSTANTS

TAB = "b_tab.png"
ST = "selected_tab.png"
ST_DARK = "st_dark.png"
SCROLL = 'scroll_down.png'
CAPTCHA = "captcha.png"
CAPTCHA_APPR = "captcha_appr.png"
ROLL_BTN = "roll_btn.png"
RELOAD_BTN = "reload.png"

TAB_REGION = (674, 17, 1245, 20)
ST_REGION = (900, 7, 989, 40)
CAPTCHA_REGION = (1126, 785, 674, 90)
ROLL_REGION = (1200, 860, 600, 90)
RELOAD_REGION = (674, 48, 1000, 30)
SCROLL_DOWN_REGION = (1890, 1030, 29, 49)

PIXELS_TO_GO_DOWN = 450
CLICKS_TO_SCROLL = -12

CLICK_COUNT = 1


# FUNCTION DEFINITIONS

def get_current_mouse_position() -> Tuple[int, int]:
    return pyautogui.position()


def return_cursor_to_initial_position(x: int, y: int) -> None:
    pyautogui.moveTo(x, y)


def fast_click_found_box(coordinates: Box) -> None:
    pyautogui.click(coordinates)


def find_bitcoin_tab() -> Box:
    return pyautogui.locateOnScreen(TAB, region=TAB_REGION, confidence=0.7)


def find_and_click_bitcoin_tab() -> Box:
    # we may wait for the algo to be initiated
    while True:

        tab_box = find_bitcoin_tab()

        if tab_box:
            print(f'\r{strftime("%H:%M:%S")}', end=" ")
            print("Tab found...", end=" ")
            fast_click_found_box(tab_box)
            print("and clicked.", end=" ")
            pyautogui.sleep(0.2)
            return tab_box
        else:
            pyautogui.sleep(0.5)


def scroll_down_the_page(tab_box: Box) -> None:
    def scrollbar_is_down() -> Box:
        return pyautogui.locateOnScreen(
            SCROLL, region=SCROLL_DOWN_REGION, confidence=0.95
        )

    while not scrollbar_is_down():
        pyautogui.scroll(CLICKS_TO_SCROLL, tab_box[0], PIXELS_TO_GO_DOWN)
        pyautogui.sleep(0.1)


def find_captcha() -> Box:
    return pyautogui.locateOnScreen(
        CAPTCHA, region=CAPTCHA_REGION, confidence=0.5
    )


def slow_captcha_click(captcha_coordinates: Box) -> None:
    pyautogui.mouseDown(captcha_coordinates)
    pyautogui.sleep(0.2)
    pyautogui.mouseUp()
    print("and clicked.", end=" ")
    pyautogui.sleep(0.2)


def find_and_click_captcha(tab_box: Box) -> None:
    captcha_search_time_limit = 50  # ~10 sec
    wait_period = 0.2

    for i in range(captcha_search_time_limit):
        captcha_box = find_captcha()
        if captcha_box:
            print("Captcha found...", end=" ")
            slow_captcha_click(captcha_box)
            return
        else:
            print("Captcha not found...", end=" ")
            scroll_down_the_page(tab_box)
            pyautogui.sleep(wait_period)


def find_captcha_approvement() -> Box:
    return pyautogui.locateOnScreen(
        CAPTCHA_APPR, region=CAPTCHA_REGION, confidence=0.8
    )


def is_captcha_approved(tab_box: Box) -> bool:
    time_limit = 50  # ~10 sec
    wait_period = 0.2

    for i in range(time_limit):
        if find_captcha_approvement():

            print(
                f"Captcha ok, time limit: "
                f"{i*wait_period}/"
                f"{time_limit*wait_period}.",
                end=" "
            )
            return True
        pyautogui.sleep(wait_period)
        scroll_down_the_page(tab_box)

    print("Captcha approvement time limit exceeded")
    return False


def find_roll_btn() -> Box:
    return pyautogui.locateOnScreen(
        ROLL_BTN, region=ROLL_REGION, confidence=0.8
    )


def is_roll_btn_clicked(tab_box) -> bool:
    # maybe unnecessary loop (guaranteed to find)
    attempts = 5
    for i in range(attempts):
        roll_box = find_roll_btn()
        if roll_box:
            print("Roll btn found.", end=" ")
            fast_click_found_box(roll_box)
            print(f"Clicked {CLICK_COUNT}.")
            return True
        else:
            print("Roll btn not found", end=" ")
            scroll_down_the_page(tab_box)
    return False


def reload_page() -> None:
    reload_box = pyautogui.locateOnScreen(
        RELOAD_BTN, region=RELOAD_REGION, confidence=0.8
    )
    pyautogui.click(reload_box)
    print("RELOADING", end=" ")


def get_currently_selected_tab() -> Box:
    tab_left_part_loc = pyautogui.locateOnScreen(
        ST, region=ST_REGION, confidence=0.8
    ) or \
        pyautogui.locateOnScreen(
        ST_DARK, region=ST_REGION, confidence=0.8
    )
    # making sure we click then tabs' icon
    if tab_left_part_loc:
        tab_icon_loc = Box(tab_left_part_loc[0] + 6, *tab_left_part_loc[1:])
    else:
        tab_icon_loc = tab_left_part_loc
    print(f"Currently selected tab: {tab_icon_loc}")
    return tab_icon_loc


def return_selection_to_prev_tab(coordinates: Box) -> None:
    pyautogui.click(coordinates)


def switch_window_context() -> None:
    pyautogui.hotkey('alt', 'tab')


def is_tab_selected():
    pass


############
###SCRIPT###
############

# outer cycle, clicking process repeates every hour (according to site)
while True:

    x_cur, y_cur = get_current_mouse_position()
    cur_selected_tab = get_currently_selected_tab()

    tab_box = find_and_click_bitcoin_tab()

    # SCROLL LOOP
    # ensuring scroll to bottom (in order to regions to work)
    # and then clicking captcha and roll button
    max_attempts = 5
    cur_attempt = 0
    while True:

        cur_attempt += 1
        if cur_attempt > max_attempts:
            reload_page()
            return_selection_to_prev_tab(cur_selected_tab)
            return_cursor_to_initial_position(x_cur, y_cur)
            break

        scroll_down_the_page(tab_box)

        find_and_click_captcha(tab_box)

        if is_captcha_approved(tab_box):

            if is_roll_btn_clicked(tab_box):

                CLICK_COUNT += 1

                return_selection_to_prev_tab(cur_selected_tab)
                return_cursor_to_initial_position(x_cur, y_cur)
                switch_window_context()

                pyautogui.sleep(60 * 60)
                break  # from scroll loop
            else:
                reload_page()
                return_selection_to_prev_tab(cur_selected_tab)
                return_cursor_to_initial_position(x_cur, y_cur)
                break
        else:
            fast_click_found_box(tab_box)  # remove selection from captcha
