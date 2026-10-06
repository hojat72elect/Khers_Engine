from ursina import Ursina, Cube, EditorCamera, color
from ursina.entity import Entity

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model=Cube(subdivisions=(3,3,3), mode='line'), color=color.red)
    e = Entity(model=Cube(subdivisions=(1,1,1), mode='line'), color=color.green, x=2)
    _ed = EditorCamera(rotation_speed = 200, panning_speed=200)
    app.run()
