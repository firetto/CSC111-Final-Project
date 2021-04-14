"""
main.py
Launch the program from here!
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import pygame
from ui_handler import add_ui
from window import Window
from board import Board
from board_manager import BoardManager

if __name__ == "__main__":

    # Initialize PyGame
    pygame.init()

    # Create a window wrapper class instance
    window = Window()

    # Add UI to the window
    add_ui(window)

    # Create a board
    board = Board()

    # TODO: REMOVE THIS!!!! This is how you access the board.
    for row in range(board.size):
        for column in range(board.size):
            d = (row + column) % 4
            if d == 1:
                board.set_piece(row, column, 1)
            elif d == 2:
                board.set_piece(row, column, -1)
            elif d == 3:
                board.set_next_move(row, column, True)

    # Setup the BoardManager instance
    board_manager = BoardManager(window)

    # Window loop
    while window.is_running():

        """ UPDATE STUFF """

        # Look at the mouse clicks and see if they are in the board.
        for event in window.get_events():
            if event[0] == pygame.MOUSEBUTTONUP:
                square = board_manager.check_mouse_press(event[1], board)
                if square != (-1, -1):
                    print("Square at ", square, " was pressed!")

        # Update the window's clock
        window.update_clock()

        """ DRAW STUFF """

        # Draw the background first!!!!
        window.draw_background()

        # Draw the board.
        board_manager.draw_board(board)

        # Draw the buttons etc.
        window.draw_ui()

        # Draw the rest of the stuff and update the window!
        window.update()

    # Once loop ends, quit pygame.
    pygame.quit()
