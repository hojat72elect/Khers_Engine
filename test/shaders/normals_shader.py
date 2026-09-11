from ursina import Ursina, window, color, Sky, EditorCamera
from ursina.prefabs.primitives import AzureSphere, GrayPlane, WhiteCube
from ursina.shaders.normals_shader import normals_shader

if __name__ == "__main__":
    app = Ursina()
    window.color = color.black
    shader = normals_shader
    a = WhiteCube(shader=shader)
    b = AzureSphere(rotation_y=180, x=3)
    b.shader = shader
    GrayPlane(scale=10, y=-2, texture="shore")
    Sky(color=color.light_gray)
    EditorCamera()

    def update():
        b.rotation_z += 1
        b.rotation_y += 1
        b.rotation_x += 1

    app.run()
