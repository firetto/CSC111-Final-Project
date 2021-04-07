"""
ui_elements.py:
Contains PyGame GUI UI element wrapper classes, for buttons, text, and more.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import pygame
import pygame_gui
import window
from typing import Tuple


class Element:
    """Generic wrapper class for UIElement and Text.

    Preconditions:
     - self._type in {"none", "button", "text"}
    """

    # Private Instance Attributes:
    # - _type: Type of the element

    _type: str

    def __init__(self, type: str = "none") -> None:
        """Basic initializer."""
        self._type = type

    def set_type(self, type: str) -> None:
        """Set the type of the element."""
        self._type = type


class UIElement(Element):
    """
    pygame_gui.core.ui_element.UIElement wrapper class, containing methods to
    change visibility, and more.
    """

    # Private Instance Attributes:
    # - _element: pygame_gui UIElement instance
    _element: pygame_gui.core.ui_element.UIElement

    def __init__(self, element: pygame_gui.core.ui_element.UIElement) -> None:
        """Instantiate self._element."""
        self._element = element

        super().__init__()

    def __eq__(self, other: pygame_gui.core.ui_element.UIElement) -> bool:
        """Return whether UIElement instance is equal to another instance."""
        return self._element == other

    def set_visible(self, visible: bool) -> None:
        """Change the visibility of the UI element."""
        self._element.visible = visible


class Button(UIElement):
    """
    pygame_gui.elements.UIButton wrapper class, containing initialization of button
    as well as 'lambda' instances to easily call the corresponding button function when it is
    pressed.
    """

    # Private Instance Attributes:
    # - _function: function to call when button is pressed
    _function: any = lambda: None

    def __init__(self, rect: pygame.Rect, label: str, manager: pygame_gui.UIManager,
                 function: any) -> None:
        """Initialize button attributes, function."""

        super().__init__(pygame_gui.elements.UIButton(relative_rect=rect,
                                                      text=label,
                                                      manager=manager))

        self._function = function

        self.set_type("button")

    def press(self) -> None:
        """Call _function()."""
        self._function()


class Text(Element):
    """
    Wrapper class for storing text to be drawn, as well as the position the text.
    """

    # Private Instance Attributes:
    # - _text: string of text that will be drawn
    # - _position: (x, y) position of text to be drawn
    # - _visible: whether the text is visible or not
    # - _large_font: whether the font is large
    _text: str
    _position: Tuple[int, int]
    _visible: bool
    _large_font: bool

    def __init__(self, text: str, position: Tuple[int, int], large_font: bool = True):
        """Initialize the text contents as well as the position of the text."""
        _text = text
        _position = position
        _visible = True
        self._large_font = large_font

        super().__init__("text")

    def set_visible(self, visible: bool) -> None:
        """Change the visibility of the text."""
        self._visible = visible

    def draw(self, window: window.Window) -> None:
        """Draw the text to a Window attribute."""

        if self._visible:

            surface = window.render_text(text=self._text, large_font=self._large_font)

            window.draw_to_screen(surface, self._position)
