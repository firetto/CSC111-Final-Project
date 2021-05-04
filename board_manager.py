"""
board_manager.py:
Contains the BoardManager class, containing board management methods.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim

Copyright 2021 Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from typing import Tuple, Union
import pygame
from window import Window
from board import Board


class BoardManager:
    """
    BoardManager class, used for drawing a board. Also contains methods for checking whether
    a square was clicked with mouse, and which one.
    """

    # Private Instance Attributes:
    # - _window: the Window instance that the board will be drawn on
    # - _BG_COLORS: A Tuple of background colors for the board
    # - _BOARD_PIXEL_SIZE: Size (in pixels) of the board
    # - _LINE_THICKNESS: How thick the lines separating each square are
    # - _BOARD_POSITION: Position of the board in the window in px, measured from top left
    # - _PIECE_COLORS: The colours of the pieces. [0] is black, [1] is white.
    # - _VALID_MOVE_COLOR: The colour of the possible next move indicator.
    # - _PIECE_RADIUS_RATIO: The ratio of piece radius to square size
    # - _VALID_MOVE_RADIUS_RATIO: The ratio of the next move indicator radius to square size
    # - _PAUSED_OVERLAY_ALPHA: The transparency of the overlay rectangle when paused (max 255)

    _window: Window

    _BG_COLORS: Tuple[pygame.Color, pygame.Color] = (pygame.Color(225, 174, 104),
                                                     pygame.Color(181, 136, 103))
    _BOARD_PIXEL_SIZE: int = 640
    _LINE_THICKNESS: int = 2
    _BOARD_POSITION: Tuple[int, int] = (20, 20)
    _PIECE_COLORS: Tuple[pygame.Color, pygame.Color] = (pygame.Color(20, 20, 20),
                                                        pygame.Color(230, 230, 230))
    _VALID_MOVE_COLOR: pygame.Color = pygame.Color(215, 146, 53)
    _PIECE_RADIUS_RATIO: float = 0.4
    _VALID_MOVE_RADIUS_RATIO: float = 0.2
    _PAUSED_OVERLAY_ALPHA: int = 100

    def __init__(self, window: Window) -> None:
        """Initialize the BoardVisualizer instance using a window and an existing
        Board class instance."""

        self._window = window

    def draw_board(self, board: Board, game_paused: bool) -> None:
        """Create a pygame.Surface of the board, then draw it to self._window.

        If game_paused is true, draw an overlay with text saying 'GAME PAUSED'"""

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
        for (row, column) in board.valid_moves:
            pygame.draw.circle(surface, self._VALID_MOVE_COLOR,
                               (column * square_size + square_size / 2,
                                row * square_size + square_size / 2),
                               square_size * self._VALID_MOVE_RADIUS_RATIO)

        # If the game is paused, draw the overlay along with text.
        if game_paused:
            overlay = pygame.Surface((self._BOARD_PIXEL_SIZE, self._BOARD_PIXEL_SIZE))
            overlay.set_alpha(self._PAUSED_OVERLAY_ALPHA)
            overlay.fill((0, 0, 0))
            surface.blit(overlay, (0, 0))
            surface.blit(self._window.render_text(text="GAME PAUSED"),
                         (self._BOARD_PIXEL_SIZE // 2 - 82, self._BOARD_PIXEL_SIZE // 2 - 12))

        self._window.draw_to_screen(surface, self._BOARD_POSITION)

    def check_mouse_press(self, position: Tuple[Union[int, float],
                                                Union[int, float]],
                          board: Board) -> Tuple[int, int]:
        """Check mouse press and return the square in (row, column) format that was pressed.
        If no square was pressed, return (-1, -1).

        Position is in (x, y) format."""

        if position[0] < self._BOARD_POSITION[0] \
                or position[0] > self._BOARD_POSITION[0] + self._BOARD_PIXEL_SIZE \
                or position[1] < self._BOARD_POSITION[1] \
                or position[1] > self._BOARD_POSITION[1] + self._BOARD_PIXEL_SIZE:
            return (-1, -1)
        else:
            # Row column format.
            pos = (position[1] - self._BOARD_POSITION[1], position[0] - self._BOARD_POSITION[0])
            square_size = (self._BOARD_PIXEL_SIZE / board.size)
            return (int(pos[0] // square_size),
                    int(pos[1] // square_size))


if __name__ == "__main__":
    # Test doctests
    import doctest
    doctest.testmod()

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['pygame', 'window', 'board'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,

        # Disable too-many-nested-blocks, too-many-arguments
        'disable': ['E1136', 'R1702', 'R0913']
    })
