from ursina import Ursina
from ursina.prefabs.main_menu import MainMenu

if __name__ == '__main__':
    app = Ursina()
    MainMenu()
    app.run()
