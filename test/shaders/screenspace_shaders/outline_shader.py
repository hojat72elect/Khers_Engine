from ursina import Ursina, color, Entity, camera, EditorCamera
from ursina.shaders.screenspace_shaders.outline_shader import outline_shader

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model='sphere', color=color.white)
    e = Entity(model='cube', y=-1)
    Entity(model='plane', scale=100, y=-10)
    camera.shader = outline_shader
    camera.far_clip_plane = 1000
    camera.set_shader_input('near', .01)

    def input(key):
        if key == 'space':
            if not camera.shader:
                camera.shader = outline_shader
            else:
                camera.shader = None

    EditorCamera()
    app.run()
