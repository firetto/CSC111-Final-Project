"""
ui_elements.py:
Contains PyGame GUI UI element wrapper classes, for buttons, text, and more.
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

from typing import Tuple, List
import pygame
import pygame_gui


class Element:
    """Generic wrapper class for UIElement and Text.

    Preconditions:
     - self._type in {"none", "button", "text", "dropdown"}
    """

    # Private Instance Attributes:
    # - _type: Type of the element

    _type: str

    def __init__(self, element_type: str = "none") -> None:
        """Basic initializer."""
        self._type = element_type

    def __eq__(self, other: pygame_gui.core.ui_element.UIElement) -> bool:
        """Return whether Element instance is equal to a UIElement instance.
        By default, this is FALSE."""
        return False

    def set_type(self, element_type: str) -> None:
        """Set the type of the element."""
        self._type = element_type

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

    def set_text(self, text: str) -> None:
        """Unimplemented method to set the text of the Text."""
        raise NotImplementedError

    def get_text(self) -> str:
        """Not implemented method to get the text of a button."""
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

    def execute(self, text: str = "") -> None:
        """Unimplemented execute method (used in Dropdown, Button)."""
        raise NotImplementedError

    def get_text(self) -> str:
        """Not implemented method to get the text of a button."""
        raise NotImplementedError

    def set_text(self, text: str) -> None:
        """Unimplemented method to set the text of the Text."""
        raise NotImplementedError


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

    def set_text(self, text: str) -> None:
        """Set the text of the button to <text>."""

        # PyCharm doesn't like this, but self._element is, by definition, a
        # pygame_gui.elements.UIButton instance for the Button class.
        self._element.set_text(text)

    def get_text(self) -> str:
        """Get the text of the button."""

        # PyCharm doesn't like this, but self._element is, by definition, a
        # pygame_gui.elements.UIButton instance for the Button class.
        return self._element.text


class Dropdown(UIElement):
    """
    pygame_gui.elements.UIDropDownMenu wrapper class, containing initialization of Dropdown
    as well as 'lambda' instances to easily call the corresponding dropdown function when the
    dropdown setting is changed.
    """

    # Private Instance Attributes:
    # - _function: function to call when the dropdown option is changed
    _function: any

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

        self._function(text)

    def set_visible(self, visible: bool) -> None:
        """Change the visibility of the dropdown."""
        self._element.visible = visible

        if visible:
            self._element.show()
        else:
            self._element.hide()

    def get_text(self) -> str:
        """Do nothing."""

    def set_text(self, text: str) -> None:
        """Do nothing."""


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

    def __init__(self, text: str, position: Tuple[int, int], large_font: bool = True) -> None:
        """Initialize the text contents as well as the position of the text."""
        self.set_text(text)
        self.position = position
        self.visible = True
        self.large_font = large_font

        super().__init__("text")

    def set_text(self, text: str) -> None:
        """Set the text of the Text."""
        self.text = text

    def execute(self, text: str = "") -> None:
        """Nothing is to be done when text is pressed."""
        return

    def set_visible(self, visible: bool) -> None:
        """Set visibility of the text."""
        self.visible = visible

    def get_visible(self) -> bool:
        """Return whether or not the text is visible."""
        return self.visible

    def get_text(self) -> str:
        """Get the text of the Text"""
        return self.text


if __name__ == "__main__":
    # Test doctests
    import doctest
    doctest.testmod(verbose=True)

    import python_ta.contracts
    python_ta.contracts.check_all_contracts()

    import python_ta
    python_ta.check_all(config={
        # the names (strs) of imported modules
        'extra-imports': ['pygame', 'pygame_gui'],
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 100,

        # Disable too-many-nested-blocks, too-many-arguments
        'disable': ['E1136', 'R1702', 'R0913']
    })
