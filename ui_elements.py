"""
ui_elements.py:
Contains PyGame GUI UI element wrapper classes, for buttons, text, and more.
CSC111 Final Project by Anatoly Zavyalov, Baker Jackson, Elliot Schrider, Rachel Kim
"""

import pygame
import pygame_gui
from typing import Tuple, List


class Element:
    """Generic wrapper class for UIElement and Text.

    Preconditions:
     - self._type in {"none", "button", "text", "dropdown"}
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

    def execute(self, text: str = "") -> None:
        """Unimplemented execute method (used in Dropdown, Button)."""
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

    def execute(self, text: str = "") -> None:
        """Call _function()."""
        self._function()


class Dropdown(UIElement):
    """
    pygame_gui.elements.UIDropDownMenu wrapper class, containing initialization of Dropdown
    as well as 'lambda' instances to easily call the corresponding dropdown function when the
    dropdown setting is changed.
    """

    # Private Instance Attributes:
    # - _function: function to call when button is pressed
    _function: any = lambda: None

    def __init__(self, options_list: List[str], starting_option: str,
                 rect: pygame.Rect, manager: pygame_gui.UIManager,
                 function: any) -> None:
        """Initialize dropdown attributes.

        Preconditions:
         - function is a lambda function that accepts a single string parameter"""

        super().__init__(pygame_gui.elements.UIDropDownMenu(
            options_list=options_list,
            starting_option=starting_option,
            relative_rect=rect,
            manager=manager
        ))

        self.set_type("dropdown")

        self._function = function

    def execute(self, text: str = "") -> None:
        """
        Execute the function corresponding to the dropdown based on the option selected.

        Preconditions:
         - text is an option of the dropdown menu
        """

        self._function()(text)

    def set_visible(self, visible: bool) -> None:
        """Change the visibility of the dropdown."""
        self._element.visible = visible

        if visible:
            self._element.show()
        else:
            self._element.hide()


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

    def execute(self, text:str = "") -> None:
        """Nothing is to be done when text is pressed."""
        return

    def set_visible(self, visible: bool) -> None:
        """Set visibility of the text."""
        self.visible = visible

    def get_visible(self) -> bool:
        """Return whether or not the text is visible."""
        return self.visible
