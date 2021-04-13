"""
ui_elements.py:
Contains PyGame GUI UI element wrapper classes, for buttons, text, and more.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import pygame
import pygame_gui
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

    def __eq__(self, other: pygame_gui.core.ui_element.UIElement) -> bool:
        """Return whether Element instance is equal to a UIElement instance.
        By default, this is FALSE."""
        return False

    def set_type(self, type: str) -> None:
        """Set the type of the element."""
        self._type = type

    def get_type(self) -> str:
        """Return the type of the element."""
        return self._type

    def set_visible(self, visible: bool) -> None:
        """Not implemented set_visible method."""
        raise NotImplementedError

    def get_visible(self) -> None:
        """Not implemented get_visible method."""
        raise NotImplementedError

    def press(self) -> None:
        """Unimplemented press method (used in Button)."""
        raise NotImplementedError


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

    def get_visible(self) -> None:
        """Return the visibility of the UI element."""
        return self._element.visible


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

    Instance Attributes:
     - text: string of text that will be drawn
     - position: (x, y) position of text to be drawn
     - visible: whether the text is visible or not
     - large_font: whether the font is large
    """

    text: str
    position: Tuple[int, int]
    visible: bool
    large_font: bool

    def __init__(self, text: str, position: Tuple[int, int], large_font: bool = True):
        """Initialize the text contents as well as the position of the text."""
        self.text = text
        self.position = position
        self.visible = True
        self.large_font = large_font

        super().__init__("text")

    def press(self) -> None:
        """Nothing is to be done when text is pressed."""
        return

    def set_visible(self, visible: bool) -> None:
        """Set visibility of the text."""
        self.visible = visible

    def get_visible(self) -> bool:
        """Return whether or not the text is visible."""
        return self.visible
