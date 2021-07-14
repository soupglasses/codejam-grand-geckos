from typing import Any, Optional

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import AnyContainer, HSplit
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.styles import BaseStyle
from prompt_toolkit.widgets import Button, Dialog, Label, TextArea, ValidationToolbar


def login_dialog(style: Optional[BaseStyle] = None) -> Application[str]:
    """
    Returns the login / register dialog application
    """

    def accept(buf: Buffer) -> bool:
        get_app().layout.focus(login_button)
        return True

    def register_handler() -> None:
        # TODO: Register
        get_app().exit(result=0)

    def login_handler() -> None:
        # TODO: Login
        get_app().exit(result=1)

    def exit_handler() -> None:
        get_app().exit()

    register_button = Button(text="Register", handler=register_handler)
    login_button = Button(text="Login", handler=login_handler)
    exit_button = Button(text="Exit", handler=exit_handler)

    username = TextArea(
        multiline=False,
        password=False,
        completer=None,
        validator=None,
        accept_handler=accept,
    )

    password = TextArea(
        multiline=False,
        password=True,
        completer=None,
        validator=None,
        accept_handler=accept,
    )

    dialog = Dialog(
        title="Login",
        body=HSplit(
            [
                Label(text="Username", dont_extend_height=True),
                username,
                Label(text="Password", dont_extend_height=True),
                password,
                ValidationToolbar(),
            ],
            padding=D(preferred=1, max=1),
        ),
        buttons=[register_button, login_button, exit_button],
        with_background=True,
    )

    return _create_app(dialog, style)


def _create_app(dialog: AnyContainer, style: Optional[BaseStyle]) -> Application[Any]:
    # Key bindings.
    bindings = KeyBindings()
    bindings.add("tab")(focus_next)
    bindings.add("s-tab")(focus_previous)

    return Application(
        layout=Layout(dialog),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=True,
    )
