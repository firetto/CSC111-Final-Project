"""
ui_handler.py
Contains methods for adding UI elements to the window.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import window
import pygame


def add_ui(w: window.Window) -> None:
    """
    Add some UI to the window, such as buttons, and more.
    :param w: a Window instance
    """
    w.add_button(rect=pygame.Rect(0, 0, 150, 50),
                 label="button-test", text="Test", function=lambda: print("hello"))
