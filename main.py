import os
import random

from dataclasses import dataclass, fields

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import webview


@dataclass
class ButtonInput:
    num_office_hours: int
    excel_file_path: str
    unavailable_hours: str

    def pyprint(self):
        fieldvals = [_ for _ in fields(self)]
        for fieldval in fieldvals:
            val = getattr(self, fieldval.name)
            if val == None: continue
            print(f"{fieldval.name}: {val}-{type(val)}")

class MainApi:
    """Main bridge for frontend javascript to execute python."""
    def __init__(self):
        self._window: webview.Window|None = None

    @property
    def window(self) -> webview.Window:
        assert self._window is not None
        return self._window
    @window.setter
    def window(self, win):
        self._window = win

    def open_file_dialog(self):
        file_types = ('Image Files (*.bmp;*.jpg;*.gif)', 'All files (*.*)')
        result = self.window.create_file_dialog(
            webview.FileDialog.OPEN, allow_multiple=True, file_types=file_types
        )
        return result;

    def _play_button_sound(self):
        button_sound = pygame.mixer.Sound(random.choice(["vova-buhh.ogg", "tyler-buhh.ogg", "ollie-buhh.ogg", "jake-buhh.ogg"]))
        button_sound.set_volume(random.choice([.7, .9, 1]))
        button_sound.play()

    def button_pressed(self, input: list):
        self._play_button_sound();
        if len(input) != len(fields(ButtonInput)): return

        button_input = ButtonInput(*input)
        button_input.pyprint()

    def pyprint(self, s):
        print("val:", s)

def main():
    pygame.mixer.init()
    api = MainApi()

    api.window = webview.create_window(
        title="Webview for Tyler AI project",
        url="./index.html",
        js_api=api,
        resizable=True,
    )

    webview.start()
    pygame.quit()

if __name__ == "__main__":
    main()
