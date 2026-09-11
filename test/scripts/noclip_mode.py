from ursina import Ursina, Entity, EditorCamera, color
from ursina.scripts.noclip_mode import NoclipMode2d

if __name__ == '__main__':
    app = Ursina()
    player = Entity(model='cube', color=color.orange)
    Entity(model='plane', scale=10)
    EditorCamera()
    player.add_script(NoclipMode2d())
    app.run()
