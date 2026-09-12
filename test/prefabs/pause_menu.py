from ursina import Ursina
from ursina.prefabs.pause_menu import PauseMenu

if __name__ == '__main__':
    app = Ursina()
    PauseMenu()
    app.run()
