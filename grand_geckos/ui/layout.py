from cryptography.fernet import Fernet
from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.widgets import HorizontalLine, Label

from grand_geckos.database.DBWorker import DatabaseWorker
from grand_geckos.ui import controls
from grand_geckos.ui.shortcuts import (
    ButtonView,
    ControlBarView,
    HorizontalSpacer,
    PanelView,
    SearchBarView,
    TitleView,
    VerticalSpacer,
)

search_bar = SearchBarView()


def generate_root(worker: DatabaseWorker, vault_key: Fernet):
    credentials = worker.user.credentials

    root = HSplit(
        [
            HorizontalSpacer(),
            TitleView(text="SECRET CRATE OF GRAND GECKOS"),
            HorizontalLine(),
            search_bar,
            HorizontalLine(),
            HorizontalSpacer(),
            VSplit(
                [
                    VerticalSpacer(),
                    PanelView(
                        title="Platform",
                        data=[
                            ButtonView(
                                vault_key.decrypt((cred.platform).encode("utf-8")).decode("utf-8"),
                                action=controls.test_action,
                            )
                            for cred in credentials
                        ],
                    ),
                    VerticalSpacer(),
                    PanelView(
                        title="Name@Username",
                        data=[
                            ButtonView(
                                vault_key.decrypt((cred.credential_name).encode("utf-8")).decode("utf-8")
                                + "@"
                                + vault_key.decrypt((cred.credential_username).encode("utf-8")).decode("utf-8"),
                                action=controls.test_action,
                            )
                            for cred in credentials
                        ],
                    ),
                    VerticalSpacer(),
                    PanelView(
                        title="Password",
                        data=[
                            Label(
                                (
                                    "*"
                                    * len(
                                        vault_key.decrypt((cred.credential_password).encode("utf-8")).decode("utf-8")
                                    )
                                )
                            )
                            for cred in credentials
                        ],
                    ),
                    VerticalSpacer(),
                ]
            ),
            HorizontalSpacer(),
            ControlBarView(
                controls=[
                    ButtonView(
                        text="Exit: Ctrl+Q",
                        action=controls.exit_app,
                    ),
                ]
            ),
            HorizontalSpacer(),
        ]
    )
    return root
