import sys

from asciimatics.exceptions import NextScene, ResizeScreenError, StopApplication
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import Button, Divider, Frame, Layout, Text, TextBox, Widget


class EditorFrame(Frame):
    box_data: str

    def __init__(self, screen):
        super().__init__(
            screen,
            screen.height,
            screen.width,
            hover_focus=True,
            can_scroll=False,
            has_border=False,
        )

        self._textbox = TextBox(Widget.FILL_FRAME, as_string=True)

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._textbox)
        layout.add_widget(Divider())

        menu_layout = Layout([1, 1])
        self.add_layout(menu_layout)
        menu_layout.add_widget(Button("Save", self._save), 0)
        menu_layout.add_widget(Button("Quit", self._quit), 1)

        self.set_theme("bright")
        self.fix()

    def _save(self):
        EditorFrame.box_data = self._textbox.value
        raise NextScene("Save")

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class SaveFrame(Frame):
    def __init__(self, screen):
        super().__init__(
            screen,
            4,
            screen.width // 2,
            hover_focus=True,
            can_scroll=False,
            has_border=False,
        )

        layout = Layout([1])
        self.add_layout(layout)
        layout.add_widget(Text("Filename:", "filename"))

        menu_layout = Layout([1, 1])
        self.add_layout(menu_layout)
        menu_layout.add_widget(Button("Write", self._write), 0)
        menu_layout.add_widget(Button("Cancel", self._cancel), 1)

        self.set_theme("bright")
        self.fix()

    def _write(self):
        self.save()
        with open(self.data["filename"], "w") as f:
            f.write(EditorFrame.box_data)
        raise NextScene("Editor")

    @staticmethod
    def _cancel():
        raise NextScene("Editor")


def demo(screen, scene):
    scenes = [
        Scene([EditorFrame(screen)], -1, name="Editor"),
        Scene([SaveFrame(screen)], -1, name="Save"),
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
