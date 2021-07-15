from prompt_toolkit.layout.containers import HSplit, VSplit
from prompt_toolkit.widgets import HorizontalLine, Label

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
                    title="Platforms",
                    data=[
                        ButtonView("Google.com", action=controls.test_action),
                        ButtonView("Facebook.com", action=controls.test_action),
                        ButtonView("My Laptop", action=controls.test_action),
                        ButtonView("HDFC Bank", action=controls.test_action),
                        ButtonView("CCTV App", action=controls.test_action),
                    ],
                ),
                VerticalSpacer(),
                PanelView(
                    title="Credentials",
                    data=[
                        ButtonView("Tommy", action=controls.test_action),
                        ButtonView("Carls", action=controls.test_action),
                        ButtonView("Robby", action=controls.test_action),
                    ],
                ),
                VerticalSpacer(),
                PanelView(
                    title="Details",
                    data=[
                        Label("Username:"),
                        Label("bigben"),
                        Label("Password:"),
                        Label("#iamapassw0rd"),
                    ],
                ),
                VerticalSpacer(),
            ]
        ),
        HorizontalSpacer(),
        ControlBarView(
            controls=[
                ButtonView(
                    text="New: Ctrl+N",
                    action=controls.new_entry,
                ),
                ButtonView(
                    text="Modify: Ctrl+E",
                    action=controls.modify_entry,
                ),
                ButtonView(
                    text="Delete: Ctrl+R",
                    action=controls.delete_entry,
                ),
                ButtonView(
                    text="Logout: Ctrl+W",
                    action=controls.logout,
                ),
                ButtonView(
                    text="Exit: Ctrl+Q",
                    action=controls.exit_app,
                ),
            ]
        ),
        HorizontalSpacer(),
    ]
)
