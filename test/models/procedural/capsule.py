from ursina import Ursina, Entity, color, EditorCamera
from ursina.models.procedural.capsule import Capsule

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model=Capsule(), texture='brick')
    origin = Entity(model='quad', color=color.orange, scale=(.05, .05), always_on_top=True)
    ed = EditorCamera(rotation_speed = 200, panning_speed=200)
    app.run()
