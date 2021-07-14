from prompt_toolkit.application import Application
from prompt_toolkit.shortcuts.dialogs import message_dialog

from grand_geckos.ui.auth import login_dialog
from grand_geckos.ui.dashboard import get_app as dashboard_app

app: Application = None


def run_app(case=None):
    global app

    if case == -1:
        app = login_dialog()

    if case == 1:
        app = dashboard_app()

    if case == 0:
        message_dialog(title="SUCCESS", text="successfully registered").run()
        app = login_dialog()

    if case == 2:
        message_dialog(title="TRY AGAIN", text="incorrect username/password").run()
        app = login_dialog()

    if case is None:
        return

    resp = app.run()
    run_app(resp)
