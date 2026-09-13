from ursina import Ursina, Entity, camera, color, EditorCamera, Sky
from ursina.shaders.screenspace_shaders.camera_grayscale import camera_grayscale_shader

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    camera.shader = camera_grayscale_shader
    EditorCamera()

    def input(key):
        if key == 'space':
            if camera.shader:
                camera.shader = None
            else:
                camera.shader = camera_grayscale_shader

    Sky()
    app.run()
