from ursina import Ursina
from ursina.prefabs.ascii_editor import ASCIIEditor

if __name__ == '__main__':

    app = Ursina()
    editor = ASCIIEditor()
    app.run()
