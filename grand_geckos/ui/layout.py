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


def generate_root(worker: DatabaseWorker):
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
                        data=[ButtonView(cred.platform, action=controls.test_action) for cred in credentials],
                    ),
                    VerticalSpacer(),
                    PanelView(
                        title="Name@Username",
                        data=[
                            ButtonView(cred.name + "@" + cred.credential_username, action=controls.test_action)
                            for cred in credentials
                        ],
                    ),
                    VerticalSpacer(),
                    PanelView(
                        title="Password",
                        data=[Label(("*" * len(cred.credential_password))) for cred in credentials],
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
