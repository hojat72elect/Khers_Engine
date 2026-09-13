from ursina import Ursina, Entity, color, camera, EditorCamera, Sky
from ursina.shaders.screenspace_shaders.camera_empty import camera_empty_shader

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model='sphere', color=color.yellow)
    e = Entity(model='cube', y=-1)
    camera.shader = camera_empty_shader
    camera.set_shader_input('contrast', 1)
    EditorCamera()
    Sky()
    app.run()
