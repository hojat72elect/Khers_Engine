from ursina import Ursina, Text
from ursina.prefabs.file_browser import FileBrowser

if __name__ == "__main__":
    app = Ursina()
    fb = FileBrowser(file_types=(".*"), enabled=False)

    def on_submit(paths):
        print("--------", paths)
        for p in paths:
            print("---", p)

    fb.on_submit = on_submit
    Text("Press Tab to open file browser", origin=(0, 0), z=1)

    def input(key):
        if key == "tab":
            fb.enabled = not fb.enabled

    app.run()
