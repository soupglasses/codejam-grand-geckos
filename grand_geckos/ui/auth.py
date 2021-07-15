from prompt_toolkit.shortcuts import button_dialog, input_dialog, message_dialog

from grand_geckos.database.DBWorker import DatabaseWorker
from grand_geckos.database.exceptions import AuthenticationError, UserAlreadyExistsError
from grand_geckos.ui.dashboard import get_app as dashboard_app


def run_app_init():
    while True:
        result = button_dialog(
            title="Welcome",
            text="Please choose an option.",
            buttons=[("Register", True), ("Login", False), ("Exit", None)],
        ).run()
        if result is True:
            text_username = input_dialog(title="Register - Username", text="Please type your username").run()
            if text_username is None:
                continue
            text_pass = input_dialog(
                title="Register - Password", text="Please type your password:", password=True
            ).run()
            if text_pass is None:
                continue
            text_pass_confirm = input_dialog(
                title="Register - Password-Confirm", text="Please type your password again:", password=True
            ).run()
            if text_pass_confirm is None:
                continue
            try:
                worker = DatabaseWorker.create_user(
                    username=text_username, password=text_pass, password_confirm=text_pass_confirm
                )
            except UserAlreadyExistsError as e:
                message_dialog(title="Error!", text=str(e)).run()
                continue
            message_dialog(title="Successful registration!", text="").run()
            dashboard_app(worker).run()

        elif result is False:
            text_username = input_dialog(title="Login - Username", text="Please type your username").run()
            if text_username is None:
                continue
            text_pass = input_dialog(title="Login - Password", text="Please type your password:", password=True).run()
            if text_pass is None:
                continue
            try:
                worker = DatabaseWorker.auth_user(username=text_username, password=text_pass)
            except AuthenticationError as e:
                message_dialog(title="Error!", text=str(e)).run()
                continue

            message_dialog(title="Successful login!", text="").run()
            dashboard_app(worker).run()
        elif result is None:
            exit()
