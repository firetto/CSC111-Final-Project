"""
main.py
Launch the program from here!
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import pygame
from ui_handler import add_ui
from window import Window

if __name__ == "__main__":

    # Initialize PyGame
    pygame.init()

    # Create a window wrapper class instance
    window = Window()

    # Add UI to the window
    add_ui(window)

    # Window loop
    while window.is_running():

        """ UPDATE STUFF """

        # Update the window's clock
        window.update_clock()

        """ DRAW STUFF """

        # Draw the background first!!!!
        window.draw_background()

        # Draw the buttons etc.
        window.draw_ui()

        # Draw the rest of the stuff and update the window!
        window.update()

    # Once loop ends, quit pygame.
    pygame.quit()
