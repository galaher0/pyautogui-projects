# coding=utf-8

import pyautogui
from time import strftime
from pyscreeze import Box
from typing import Tuple


# CONSTANTS

# TODO refactor constants to enums
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


class InitialState:
    """Saves and restores initial mouse position and browser tab selection"""

    _x_cur: int
    _y_cur: int
    _selected_tab: int

    def save_state(self):
        self._x_cur, self._y_cur = self._get_current_mouse_position()
        self._selected_tab = self._get_currently_selected_tab()

    def restore_state(self):
        """the order of funcs matters"""
        self._return_selection_to_prev_tab()
        self._return_cursor_to_initial_position()
        self._switch_window_context()

    def _get_current_mouse_position(self) -> Tuple[int, int]:
        return pyautogui.position()

    def _return_cursor_to_initial_position(self) -> None:
        pyautogui.moveTo(self._x_cur, self._y_cur)

    def _get_currently_selected_tab(self) -> Box:
        tab_left_part_loc = pyautogui.locateOnScreen(
            ST, region=ST_REGION, confidence=0.8
        ) or \
            pyautogui.locateOnScreen(
            ST_DARK, region=ST_REGION, confidence=0.8
        )
        # making sure we click then tabs' icon
        if tab_left_part_loc:
            tab_icon_loc = Box(tab_left_part_loc[0] + 6,
                               *tab_left_part_loc[1:])
        else:
            tab_icon_loc = tab_left_part_loc
        print(f"Currently selected tab: {tab_icon_loc}")
        return tab_icon_loc

    def _return_selection_to_prev_tab(self) -> None:
        pyautogui.click(self._selected_tab)

    def _switch_window_context(self) -> None:
        pyautogui.hotkey('alt', 'tab')


class Logger:
    """Controls logging to stdout"""

    msg_ongoing: bool = False

    def _update_message(self, msg_chunk: str, end: bool = False) -> None:

        if not self.msg_ongoing:
            print(f'\r{strftime("%H:%M:%S")}', end=" ", flush=True)
            self.msg_ongoing = True

        if not end:
            print(msg_chunk, end=" ", flush=True)
        else:
            print(msg_chunk)
            self.msg_ongoing = False

    def add_to_msg(self, msg_chunk: str) -> None:
        self._update_message(msg_chunk)

    def end_msg_with(self, end_msg_chunk: str) -> None:
        self._update_message(end_msg_chunk, end=True)


logger = Logger()

# FUNCTION DEFINITIONS

def fast_click_found_box(coordinates: Box) -> None:
    pyautogui.click(coordinates)


def find_bitcoin_tab() -> Box:
    return pyautogui.locateOnScreen(TAB, region=TAB_REGION, confidence=0.7)


def find_and_click_bitcoin_tab() -> Box:
    # we may wait for the algo to be initiated
    while True:

        tab_box = find_bitcoin_tab()

        if tab_box:
            logger.add_to_msg("Tab found...")
            fast_click_found_box(tab_box)
            logger.add_to_msg("and clicked.")
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
    logger.add_to_msg("and clicked.")
    pyautogui.sleep(0.2)


def find_and_click_captcha(tab_box: Box) -> None:
    captcha_search_time_limit = 25  # ~5 sec
    appr_time_limit = 10  # ~2 sec
    wait_period = 0.2

    for i in range(captcha_search_time_limit):
        captcha_box = find_captcha()
        if captcha_box:
            logger.add_to_msg("Captcha found...")
            slow_captcha_click(captcha_box)
            for j in range(appr_time_limit):
                if is_captcha_approved(tab_box):
                    logger.add_to_msg(
                        f"Captcha ok, time limit: "
                        f"{j*wait_period}/"
                        f"{appr_time_limit*wait_period}."
                    )
                    return True
                else:
                    slow_captcha_click(captcha_box)
                    pyautogui.sleep(wait_period)
            logger.end_msg_with("Captcha approvement time limit exceeded")
        else:
            logger.add_to_msg("Captcha not found...")
            scroll_down_the_page(tab_box)
            pyautogui.sleep(wait_period)
    return False


def find_captcha_approvement() -> Box:
    return pyautogui.locateOnScreen(
        CAPTCHA_APPR, region=CAPTCHA_REGION, confidence=0.8
    )


def is_captcha_approved(tab_box: Box) -> bool:
    if find_captcha_approvement():
        return True
    scroll_down_the_page(tab_box)
    return False


def find_roll_btn() -> Box:
    return pyautogui.locateOnScreen(
        ROLL_BTN, region=ROLL_REGION, confidence=0.8
    )


def is_roll_btn_clicked(tab_box: Box) -> bool:
    # maybe unnecessary loop (guaranteed to find)
    attempts = 5
    for i in range(attempts):
        roll_box = find_roll_btn()
        if roll_box:
            logger.add_to_msg("Roll btn found.")
            fast_click_found_box(roll_box)
            logger.end_msg_with(f"Clicked {CLICK_COUNT}.")
            return True
        else:
            logger.add_to_msg("Roll btn not found")
            scroll_down_the_page(tab_box)
    return False


def reload_page() -> None:
    reload_box = pyautogui.locateOnScreen(
        RELOAD_BTN, region=RELOAD_REGION, confidence=0.8
    )
    pyautogui.click(reload_box)
    logger.add_to_msg("RELOADING")


def is_tab_selected():
    pass


############
###SCRIPT###
############

state = InitialState()
# clicking process repeates every hour (according to site mechanics)
while True:

    state.save_state()

    tab_box = find_and_click_bitcoin_tab()

    scroll_down_the_page(tab_box)

    if not find_and_click_captcha(tab_box):
        find_and_click_bitcoin_tab()
        reload_page()
        state.restore_state()
        continue

    if is_roll_btn_clicked(tab_box):

        CLICK_COUNT += 1

        state.restore_state()

        pyautogui.sleep(60 * 60)
    else:
        reload_page()
        state.restore_state()
