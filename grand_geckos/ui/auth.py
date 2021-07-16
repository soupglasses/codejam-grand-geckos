from cryptography.fernet import Fernet
from prompt_toolkit.shortcuts import button_dialog, input_dialog, message_dialog
from prompt_toolkit.styles import Style

from grand_geckos.database.DBWorker import DatabaseWorker
from grand_geckos.database.exceptions import (
    AuthenticationError,
    PasswordMismatch,
    PasswordNotStrongEnough,
    UserAlreadyExistsError,
)
from grand_geckos.database.models import Credential
from grand_geckos.ui.dashboard import get_app as dashboard_app

dialog_style = Style.from_dict(
    {
        "dialog": "bg:#ffa500",
        "dialog frame.label": "bg:#000000 #ffff00",
        "dialog.body": "bg:#000000 #ffff00",
        "dialog shadow": "bg:#111111",
        "button.focused": "bg:#ffa500 #ffffcc",
        "text-area": "bg:#111111 #ffffaa",
    }
)


def main_menu(worker: DatabaseWorker, vault_key: Fernet, text_pass: str):
    result = button_dialog(
        title="Done!",
        text="What's next?",
        buttons=[
            ("Vault", True),
            ("New Credential", False),
        ],
        style=dialog_style,
    ).run()
    if result:
        dashboard_app(worker, vault_key).run()
    else:
        text_credential_name = input_dialog(
            title="What would you like to name this credential? (eg. Github Work, Raspberry Pi4, SSH-hobby)",
            text="",
            style=dialog_style,
        ).run()

        text_credential_username = input_dialog(
            title="Username - Credential", text="Please type in the username for the credential", style=dialog_style
        ).run()
        text_credential_password = input_dialog(
            title="Password - Credential",
            text="Please type in the password for the credential",
            password=True,
            style=dialog_style,
        ).run()
        text_platform = input_dialog(
            title="Credential Platform (eg. github.com, mail.google.com, ssh)", text="", style=dialog_style
        ).run()
        cred = Credential(
            credential_name=text_credential_name,
            actual_password=text_pass,
            credential_username=text_credential_username,
            platform=text_platform,
            credential_password=text_credential_password,
            user=worker.user,
        )
        worker.append_credential(cred)
        dashboard_app(worker, vault_key).run()
    return


def run_app_init() -> None:
    """Function that contains dialogs of Auth interactions such as Login,Register"""
    while True:
        result = button_dialog(
            title="Welcome",
            text="Please choose an option.",
            buttons=[("Register", True), ("Login", False), ("Exit", None)],
            style=dialog_style,
        ).run()
        # Registration Process - Register
        if result is True:
            text_username = input_dialog(
                title="Register - Username", text="Please type your username", style=dialog_style
            ).run()
            if text_username is None:
                continue
            text_pass = input_dialog(
                title="Register - Password", text="Please type your password:", password=True, style=dialog_style
            ).run()
            if text_pass is None:
                continue
            text_pass_confirm = input_dialog(
                title="Register - Password-Confirm",
                text="Please type your password again:",
                password=True,
                style=dialog_style,
            ).run()
            if text_pass_confirm is None:
                continue
            try:
                worker = DatabaseWorker.create_user(
                    username=text_username, password=text_pass, password_confirm=text_pass_confirm
                )
            except (UserAlreadyExistsError, PasswordNotStrongEnough, PasswordMismatch) as e:
                message_dialog(title="Oops, something went wrong!", text=str(e), style=dialog_style).run()
                continue
            vault_key = worker.vault_key(worker.user, text_pass)
            message_dialog(title="Successful registration!", text="", style=dialog_style).run()
            main_menu(worker, vault_key, text_pass)
        # Login Process - Login
        elif result is False:
            text_username = input_dialog(
                title="Login - Username", text="Please type your username", style=dialog_style
            ).run()
            if text_username is None:
                continue
            text_pass = input_dialog(
                title="Login - Password", text="Please type your password:", password=True, style=dialog_style
            ).run()
            if text_pass is None:
                continue
            try:
                worker = DatabaseWorker.auth_user(username=text_username, password=text_pass)
            except AuthenticationError as e:
                message_dialog(title="Error!", text=str(e), style=dialog_style).run()
                continue

            vault_key = worker.vault_key(worker.user, text_pass)
            message_dialog(title="Successful login!", text="", style=dialog_style).run()
            main_menu(worker, vault_key, text_pass)
        # Exit
        elif result is None:
            exit()
