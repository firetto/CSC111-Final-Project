"""
ui_handler.py
Contains methods for adding UI elements to the window.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import window
import pygame


def toggle_lights(w: window.Window) -> None:
    """
    TEST FUNCTION, TO BE REMOVED!

    TODO: REMOVE THIS FROM PRODUCTION BUILD
    """

    w.get_ui_element("text-test").set_visible(not w.get_ui_element("text-test").get_visible())
    w.get_ui_element("button-test-hello").set_visible(
        not w.get_ui_element("button-test-hello").get_visible())
    w.get_ui_element("dropdown-test").set_visible(
        not w.get_ui_element("dropdown-test").get_visible())


def dropdown_test(text: str) -> None:
    """
    TEST FUNCTION, TO BE REMOVED!!!!!

    TODO: REMOVE THIS FROM PRODUCTION BUILD
    """

    print(text)


def add_ui(w: window.Window) -> None:
    """
    Add some UI to the window, such as buttons, and more.
    :param w: a Window instance
    """
    w.add_button(rect=pygame.Rect(700, 20, 150, 50),
                 label="button-test-lights", text="Toggle lights",
                 function=lambda: toggle_lights(w))

    w.add_dropdown(options_list=["One", "Two", 'Three'],
                   starting_option="One",
                   rect=pygame.Rect(700, 100, 150, 50),
                   label="dropdown-test",
                   function=dropdown_test)

    w.add_text(label="text-test", text="BOO!", position=(700, 500))

    w.add_button(rect=pygame.Rect(700, 200, 150, 50),
                 label="button-test-hello", text="Say Hello",
                 function=lambda: print("Hello!"))
