from ursina import Ursina, Cylinder, color, EditorCamera
from ursina.entity import Entity

if __name__ == '__main__':
    app = Ursina()
    Entity(model=Cylinder(6, start=-0.5), texture="brick")
    origin = Entity(model="quad", color=color.orange, scale=(5, 0.05))
    ed = EditorCamera(rotation_speed=200, panning_speed=200)
    app.run()
