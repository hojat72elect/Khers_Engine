from ursina import Ursina, Entity, camera, EditorCamera, color, Vec3
from ursina.shaders.screenspace_shaders.curvature_shader import curvature_shader
import random

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    camera.shader = curvature_shader
    camera.clip_plane_near = 1
    EditorCamera()
    random.seed(2)

    for i in range(20):
        e = Entity(model='cube', position=Vec3(random.random(),random.random(),random.random())*2, rotation=Vec3(random.random(),random.random(),random.random())*360)

    app.run()
