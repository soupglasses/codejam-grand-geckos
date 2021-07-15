from typing import Any, Dict

from prompt_toolkit.application import Application
from prompt_toolkit.shortcuts.dialogs import message_dialog

from grand_geckos.ui.auth import login_dialog
from grand_geckos.ui.dashboard import get_app as dashboard_app

app: Application = None


def run_app(case=None, title_text=None, message_text=None):
    """handle running of multiple pages/apps"""
    global app

    if case == 0:
        # display login page with an optional message dialog before
        if title_text is not None and message_text is not None:
            message_dialog(title=title_text, text=message_text).run()
        app = login_dialog()

    if case == 1:
        # display dashboard page with an optional message dialog before
        if title_text is not None and message_text is not None:
            message_dialog(title=title_text, text=message_text).run()
        app = dashboard_app()

    response: Dict[str, Any] = app.run()
    if response is None:
        # exit app
        return

    res_case = response.get("case")
    res_title_text = response.get("title")
    res_message_text = response.get("text")
    run_app(res_case, res_title_text, res_message_text)
