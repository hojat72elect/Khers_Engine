from ursina import color
from ursina.entity import Entity
from ursina.vec3 import Vec3
from ursina.input_handler import held_keys
from ursina.main import Ursina
from ursina.prefabs.draggable import Draggable
from ursina.prefabs.editor_camera import EditorCamera
from ursina.models.procedural.cone import Cone
from ursina.scene import instance as scene
from ursina.models.procedural.grid import Grid
import time

if __name__ == '__main__':
    app = Ursina()
    draggable = Draggable(parent=scene, model="cube", plane_direction=Vec3.up)
    turret = Entity(model=Cone(), scale=Vec3(0.5, 1, 0.5), origin_y=-0.5, color=color.azure)
    turret.model.colorize()
    grid = Entity(model=Grid(8, 8), scale=8, rotation_x=90)

    def update():
        turret.lookAt(draggable.position, Vec3.up)
        draggable.y += (held_keys['e'] - held_keys['q']) * time.dt * 10

    EditorCamera()
    app.run()
