"""
board_visualizer.py:
Contains the BoardVisualizer class, used for drawing the board.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import pygame
from window import Window
from board import Board


class BoardVisualizer:
    """
    BoardVisualizer class, used for drawing a board.
    """

    # Private Instance Attributes:
    # - _window: the Window instance that the board will be drawn on
    # - _BG_COLORS: A Tuple of background colors for the board
    # - _BOARD_PIXEL_SIZE: Size (in pixels) of the board
    # - _LINE_THICKNESS: How thick the lines separating each square are
    # - _BOARD_POSITION: Position of the board in the window in px, measured from top left
    # - _PIECE_COLORS: The colours of the pieces. [0] is black, [1] is white.
    # - _NEXT_MOVE_COLOR: The colour of the possible next move indicator.
    # - _PIECE_RADIUS_RATIO: The ratio of piece radius to square size
    # - _NEXT_MOVE_RADIUS_RATIO: The ratio of the next move indicator radius to square size

    _window: Window

    _BG_COLORS = (pygame.Color(225, 174, 104), pygame.Color(181, 136, 103))
    _BOARD_PIXEL_SIZE = 640
    _LINE_THICKNESS = 4
    _BOARD_POSITION = (20, 20)
    _PIECE_COLORS = (pygame.Color(20, 20, 20), pygame.Color(230, 230, 230))
    _NEXT_MOVE_COLOR = pygame.Color(215, 146, 53)
    _PIECE_RADIUS_RATIO = 0.4
    _NEXT_MOVE_RADIUS_RATIO = 0.2

    def __init__(self, window: Window) -> None:
        """Initialize the BoardVisualizer instance using a window and an existing
        Board class instance."""

        self._window = window

    def draw_board(self, board: Board) -> None:
        """Create a pygame.Surface of the board, then draw it to self._window"""

        # Size of each square in pixels.
        square_size = self._BOARD_PIXEL_SIZE / board.size

        # Create an empty surface to draw onto
        surface = pygame.Surface((self._BOARD_PIXEL_SIZE, self._BOARD_PIXEL_SIZE))

        # Draw the main color of the board
        pygame.draw.rect(surface, self._BG_COLORS[0],
                         pygame.Rect(0, 0, self._BOARD_PIXEL_SIZE, self._BOARD_PIXEL_SIZE))

        # Draw the lines to separate the squares
        for i in range(1, board.size):
            # Draw horizontal lines
            pygame.draw.rect(surface, self._BG_COLORS[1],
                             pygame.Rect(0, i * square_size - self._LINE_THICKNESS / 2,
                                         self._BOARD_PIXEL_SIZE, self._LINE_THICKNESS))
            # Draw vertical lines
            pygame.draw.rect(surface, self._BG_COLORS[1],
                             pygame.Rect(i * square_size - self._LINE_THICKNESS / 2, 0,
                                         self._LINE_THICKNESS, self._BOARD_PIXEL_SIZE))

        # Draw pieces!
        for row in range(board.size):
            for column in range(board.size):
                piece = board.get_piece(row=row, column=column)

                if piece == 0:  # Empty piece
                    continue
                elif piece == 1:  # Black
                    piece_color = self._PIECE_COLORS[0]
                else:  # White
                    # assert piece == -1
                    piece_color = self._PIECE_COLORS[1]
                pygame.draw.circle(surface, piece_color,
                                   (column * square_size + square_size / 2,
                                    row * square_size + square_size / 2),
                                   square_size * self._PIECE_RADIUS_RATIO)

        # Draw next move indicators.
        for (row, column) in board.next_moves:
            pygame.draw.circle(surface, self._NEXT_MOVE_COLOR,
                               (column * square_size + square_size / 2,
                                row * square_size + square_size / 2),
                               square_size * self._NEXT_MOVE_RADIUS_RATIO)

        self._window.draw_to_screen(surface, self._BOARD_POSITION)
