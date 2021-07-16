from prompt_toolkit.application import Application
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.shortcuts import set_title

from grand_geckos.ui.bindings import global_bindings
from grand_geckos.ui.layout import generate_root, title
from grand_geckos.ui.style import global_style


def get_app(worker, vault_key, theme=global_style):
    application = Application(
        layout=Layout(generate_root(worker, vault_key), focused_element=title),
        key_bindings=global_bindings(),
        style=theme,
        mouse_support=True,
        full_screen=True,
    )
    set_title("SECRET CRATE OF GRAND GECKOS")
    return application
