"""
main.py
Launch the program from here!
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import pygame
from ui_handler import add_ui
from window import Window
from reversi import ReversiGame
from board import Board
from board_manager import BoardManager
from ai_players import RandomPlayer, MinimaxPlayer

if __name__ == "__main__":

    # Initialize PyGame
    pygame.init()

    # Create a window wrapper class instance
    window = Window()

    # Add UI to the window
    add_ui(window)

    # Create a ReversiGame instance
    game = ReversiGame()

    # Setup the BoardManager instance
    board_manager = BoardManager(window)

    # Minimax Player

    player = MinimaxPlayer(4)

    # Window loop
    while window.is_running():

        """ UPDATE STUFF """

        # Look at the mouse clicks and see if they are in the board.
        for event in window.get_events():
            if event[0] == pygame.MOUSEBUTTONUP:
                square = board_manager.check_mouse_press(event[1], game.get_board())
                if square != (-1, -1):
                    print("CLICK!!! Row: ", square[1], "; Column: ", square[0])
                    game.try_make_move(square)
                    print(game.get_winner())
                    if game.get_winner() is None:
                        game.try_make_move(player.make_move(game, square))

        # Update the window's clock
        window.update_clock()

        """ DRAW STUFF """

        # Draw the background first!!!!
        window.draw_background()

        # Draw the board.
        board_manager.draw_board(game.get_board())

        # Draw the buttons etc.
        window.draw_ui()

        # Draw the rest of the stuff and update the window!
        window.update()

    # Once loop ends, quit pygame.
    pygame.quit()
