import webview

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

    def nullfunc(self, file:str) -> None:
        print(f"nullfunc called from file:{file.split("/")[-1]}")

def main():
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
