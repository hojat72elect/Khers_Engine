from ursina import Ursina, color, camera
from ursina.entity import Entity
from ursina.vec3 import Vec3
from ursina.prefabs.editor_camera import EditorCamera
from ursina.prefabs.button import Button
from ursina.prefabs.sky import Sky
from ursina.shaders.screenspace_shaders.ssao import ssao_shader
import random

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    e = Entity(model='plane', scale=100, y=-1)
    Sky()
    Button(y=-.4, scale=.1)
    camera.shader = ssao_shader
    EditorCamera()

    def input(key):
        if key == 'space':
            if camera.shader:
                camera.shader = None
            else:
                camera.shader = ssao_shader

    random.seed(2)

    for i in range(20):
        e = Entity(model='cube', position=Vec3(random.random(),random.random(),random.random())*3, rotation=Vec3(random.random(),random.random(),random.random())*360)

    app.run()
