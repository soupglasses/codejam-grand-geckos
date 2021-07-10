from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Frame, Layout, TextBox, Widget


class EditorFrame(Frame):
    def __init__(self, screen):
        super().__init__(
            screen,
            screen.height,
            screen.width,
            hover_focus=True,
            can_scroll=False,
            has_border=False,
        )

        self._textbox = TextBox(
            Widget.FILL_FRAME,
        )

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._textbox)

        self.set_theme("bright")
        self.fix()


def demo(screen):
    scenes = [Scene([EditorFrame(screen)], -1, name="Editor")]

    screen.play(scenes, stop_on_resize=True)


Screen.wrapper(demo)
