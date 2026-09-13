from ursina import Ursina, Sprite, color
from ursina.prefabs.ursfx import UrsfxGUI

if __name__ == '__main__':
    app = Ursina()
    sfx_editor = UrsfxGUI()
    Sprite('shore', z=10, ppu=64, color=color.gray)
    app.run()
