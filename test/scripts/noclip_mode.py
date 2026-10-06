from ursina import Ursina, EditorCamera, color
from ursina.scripts.noclip_mode import NoclipMode2d
from ursina.entity import Entity

if __name__ == '__main__':
    app = Ursina()
    player = Entity(model='cube', color=color.orange)
    Entity(model='plane', scale=10)
    EditorCamera()
    player.add_script(NoclipMode2d())
    app.run()
