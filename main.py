"""
main.py
Launch the program from here!
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import pygame
from ui_handler import add_ui
from window import Window
import reversi
from reversi import ReversiGame
from board import Board
from board_manager import BoardManager
from ai_players import RandomPlayer, MinimaxPlayer
from statistics import plot_game_statistics

if __name__ == "__main__":

    # Initialize PyGame
    pygame.init()

    # Create a window wrapper class instance
    window = Window()

    # Add UI to the window
    add_ui(window)

    # Create a ReversiGame instance
    # Change human_player to 1 or -1 to play against AI
    human_p = 0
    game = ReversiGame(human_player=human_p)

    # Setup the BoardManager instance
    board_manager = BoardManager(window)

    # Minimax Player

    player1 = MinimaxPlayer(2)
    player2 = RandomPlayer()
    colour_to_player = {1: player1, -1: player2}

    # Set number of games
    num_games_left = 40

    # List of moves made
    moves_made = [(-1, -1)]

    # List of game win results
    results = []

    generated_stats = False

    # Window loop
    while window.is_running():

        """ UPDATE STUFF """

        # Look at the mouse clicks and see if they are in the board.
        winner = game.get_winner()
        if winner is not None and num_games_left > 0:
            results.append(winner)
            print(winner)
            num_games_left -= 1
            game = ReversiGame(human_player=human_p)

        if num_games_left == 0 and generated_stats is False:
            generated_stats = True
            plot_game_statistics(results, 'black')

        if game.get_human_player() == game.get_current_player():
            for event in window.get_events():
                if event[0] == pygame.MOUSEBUTTONUP:
                    square = board_manager.check_mouse_press(event[1], game.get_board())
                    if square != (-1, -1):
                        print("CLICK!!! Row: ", square[1], "; Column: ", square[0])
                        if game.try_make_move(square):
                            moves_made.append(square)
        elif game.get_winner() is None:
            moves_made.append(game.try_make_move(colour_to_player[game.get_current_player()]
                                                 .make_move(game, moves_made[-1])))

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
