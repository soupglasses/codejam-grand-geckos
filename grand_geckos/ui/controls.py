from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding.key_processor import KeyPressEvent


def test_action(event: KeyPressEvent = None):
    pass


def new_entry(event: KeyPressEvent = None):
    pass


def modify_entry(event: KeyPressEvent = None):
    pass


def delete_entry(event: KeyPressEvent = None):
    pass


def logout(event: KeyPressEvent = None):
    pass


def exit_app(event: KeyPressEvent = None):
    if event is not None:
        event.app.exit()
    else:
        get_app().exit()
