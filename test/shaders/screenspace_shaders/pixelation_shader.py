from ursina import Ursina, Entity, camera, EditorCamera, color
from ursina.shaders.screenspace_shaders.pixelation_shader import pixelation_shader

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    camera.shader = pixelation_shader
    EditorCamera()
    app.run()
