from ursina import Ursina, window, color, Entity, camera, Sky, EditorCamera
from ursina.shaders.screenspace_shaders.fxaa import fxaa_shader

if __name__ == '__main__':
    app = Ursina()
    window.color = color.black
    Entity(model="plane", scale=10, y=-2, texture="shore")
    EditorCamera()
    Entity(model="quad", color=color.red, double_sided=True)
    Entity(model="quad", color=color.green, z=-0.001, scale=0.5, texture="circle")
    camera.shader = fxaa_shader
    camera.clip_plane_far = 100
    Sky()

    def input(key):
        if key == "space":
            if not camera.shader:
                camera.shader = fxaa_shader
            else:
                camera.shader = None

    app.run()