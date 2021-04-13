"""
window.py:
Contains PyGame window wrapper class.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

from typing import Dict, List, Tuple, Set, Union
import pygame
import pygame_gui
from ui_elements import Element, Button, Text


class Window:
    """
    Window class containing window update methods and window attributes.
    Instance Attributes:
     - BACKGROUND_COLOR: The background color of the window.
     - FONT_SIZES: A tuple containing the font sizes for the largest and smallest font size.
    Sample Usage:
    >>> pygame.init()
    (7, 0)
    >>> window = Window() # wow you did it!!!
    """

    # Private Instance Attributes:
    # - _width: The width of the window (in px). Preset to be 800px.
    # - _height: The height of the window (in px). Preset to be 600px.
    # - _title: The name of the window
    # - _running: Whether the window is running. If not, the window should close.
    # - _screen: PyGame display surface
    # - _gui_manager: pygame_gui UI Manager instance
    # - _background_surface: a solid color for the surface
    # - _ui_elements: UI elements stored by the window, labelled by strings.
    # - _clock: pygame.time.Clock instance, used for updating GUI
    # - _time_delta: the time delta in milliseconds for this update
    # - _large_font: PyGame font instance, used for rendering text.
    # - _small_font: PyGame font instance, used for rendering text. Smaller font size.

    # Private Representation Invariants:
    # - self._width > 0
    # - self._height > 0

    _width: int
    _height: int
    _title: str
    _running: bool

    _ui_elements: Dict[str, Element]

    _screen: pygame.Surface
    _gui_manager: pygame_gui.UIManager
    _clock: pygame.time.Clock
    _time_delta: float

    _background_surface: pygame.Surface

    _large_font: pygame.font.Font
    _small_font: pygame.font.Font

    BACKGROUND_COLOR: Tuple[int, int, int] = (20, 40, 20)
    FONT_SIZES: Tuple[int, int] = (32, 24)

    def __init__(self) -> None:
        """Initialize window attributes, start window loop."""

        # Initialize basic window attributes
        self._running = True
        self._width = 900
        self._height = 700
        self._title = "Reversi B)"
        self._ui_elements = {}

        # Initialize Pygame stuff
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption(self._title)

        # Initialize GUI
        self._gui_manager = pygame_gui.UIManager((self._width, self._height))

        # Initialize background surface
        self._background_surface = pygame.Surface((self._width, self._height))
        self._background_surface.fill(self.BACKGROUND_COLOR)

        # Initialize clock
        self._clock = pygame.time.Clock()
        self._time_delta = 0

        # Initialize font
        self._large_font = pygame.font.Font(None, self.FONT_SIZES[0])
        self._small_font = pygame.font.Font(None, self.FONT_SIZES[1])

    def draw_background(self) -> None:
        """
        Draws the background, call this BEFORE drawing images onto the window!
        """

        # Display background surface
        self.draw_to_screen(self._background_surface, (0, 0))

    def update(self) -> None:
        """Window loop body."""

        # Update Pygame Display
        pygame.display.flip()

        # Handle window events
        self._handle_events()

        # Update GUI manager (time takes seconds and not ms, so divide by 1000)
        self._gui_manager.update(self._time_delta / 1000.0)

    def draw_ui(self) -> None:
        """Draw the buttons and sliders and so on."""
        # Draw UI
        self._gui_manager.draw_ui(self._screen)

    def _handle_events(self) -> None:
        """Handle PyGame window events"""

        for event in pygame.event.get():

            # If window is to be closed
            if event.type == pygame.QUIT:
                self._running = False

            # User event
            elif event.type == pygame.USEREVENT:

                # Check if button was pressed
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:

                    # Loop through every button, and check if it is the button that was pressed
                    # (This is kind of bad and inefficient, look for a better way to do this!)
                    for element in self._ui_elements:
                        if event.ui_element == self._ui_elements[element]:
                            if self._ui_elements[element].get_type() == "button":
                                self._ui_elements[element].press()
                            break

            self._gui_manager.process_events(event)

    def add_button(self, rect: pygame.Rect, label: str, text: str, function: any) -> None:
        """
        Add a button to list of buttons.

        label is the key for self._ui_elements, while text is the text displayed on the button.

        Preconditions:
         - len(label) > 0
         - function is of function type (callable)
         - label not in self._ui_elements
        """
        self._ui_elements[label] = Button(rect=rect, label=text,
                                          manager=self._gui_manager, function=function)

    def add_slider(self, rect: pygame.Rect, label: str,
                   start_value: float, value_range: Tuple[float, float]) -> None:
        """
        Add a slider to the dictionary of sliders.
        Preconditions:
         - label not in self._ui_elements
         - len(label) > 0
         - value_range[1] > value_range[0]
         - value_range[0] <= start_value <= value_range[1]
        """

        raise NotImplementedError

        # self._ui_elements[label] = UIHorizontalSlider(relative_rect=rect,
        #                                           start_value=start_value,
        #                                           value_range=value_range,
        #                                           manager=self._gui_manager)

    def is_running(self) -> bool:
        """
        Return whether window is running.
        """
        return self._running

    def get_screen(self) -> pygame.Surface:
        """
        Return the background screen instance.
        """
        return self._screen

    def draw_to_screen(self, surface: pygame.Surface, position: Tuple[int, int]) -> None:
        """
        Draw surface at position onto self._screen.
        """
        self._screen.blit(surface, position)

    def update_clock(self) -> None:
        """
        Update the clock and set self._time_delta to be the time delta in milliseconds.
        """
        self._time_delta = self._clock.tick(60)

    def get_delta(self) -> float:
        """
        Return the time delta in milliseconds.
        """
        return self._time_delta

    def render_text(self, text: str,
                    color: pygame.color.Color = pygame.color.Color(255, 255, 255),
                    background: pygame.color.Color = BACKGROUND_COLOR,
                    large_font: bool = True, antialias: bool = True) -> pygame.Surface:
        """
        Return the pygame Font render given the parameters.
        Preconditions:
        - len(text) > 0
        """
        if large_font:
            return self._large_font.render(text, antialias, color, background)
        else:
            return self._small_font.render(text, antialias, color, background)

    def draw_text(self, text: Text):
        """Draw a Text instance to the Window."""

        if text.visible:
            surface = w.render_text(text=text.text, large_font=text.large_font)

            w.draw_to_screen(surface, text.position)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pygame', 'pygame_gui', 'pygame_gui.elements.ui_horizontal_slider',
                          'typing', 'button', 'python_ta.contracts'],
        # the names (strs) of imported modules
        'allowed-io': [],
        # the names (strs) of functions that call print/open/input
        'max-line-length': 100,
        'disable': ['R1705', 'C0200']
    })

    import python_ta.contracts

    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
