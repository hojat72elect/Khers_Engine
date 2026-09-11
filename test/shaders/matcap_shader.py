from ursina import Ursina, window, color, Sky, EditorCamera
from ursina.prefabs.primitives import GrayPlane, WhiteCube, WhiteSphere
from ursina.shaders.matcap_shader import matcap_shader

if __name__ == "__main__":
    app = Ursina()
    window.color = color.black
    shader = matcap_shader

    a = WhiteCube(shader=shader, texture="shore")
    b = WhiteSphere(shader=shader, rotation_y=180, x=3, texture="shore")
    GrayPlane(scale=10, y=-2, texture="shore")
    Sky(color=color.light_gray)
    EditorCamera()

    def update():
        b.rotation_z += 1
        b.rotation_y += 1
        b.rotation_x += 1

    print("-----------------", repr(a.shader))
    app.run()
