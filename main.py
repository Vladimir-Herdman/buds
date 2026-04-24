import random

import pygame
import webview

class MainApi:
    """Main bridge for frontend javascript to execute python."""
    def __init__(self):
        self._window: webview.Window|None = None
        self.button_sound = pygame.mixer.Sound("vova-buhh.ogg")

    @property
    def window(self) -> webview.Window:
        assert self._window is not None
        return self._window
    @window.setter
    def window(self, win):
        self._window = win

    def play_sound(self):
        self.button_sound.set_volume(random.choice([.7, .9, 1]))
        self.button_sound.play()

    def pyprint(self, s: str):
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

if __name__ == "__main__":
    main()
