import json
from ursina import Ursina
from ursina.prefabs.file_browser_save import FileBrowserSave

if __name__ == "__main__":
    app = Ursina()
    wp = FileBrowserSave(file_type=".*")
    save_data = {"level": 4, "name": "Link"}
    wp.data = json.dumps(save_data)
    wp.enabled = False

    def input(key):
        if key == "tab":
            wp.enabled = not wp.enabled

    app.run()
