from ursina import Ursina, window, Sky, EditorCamera, color, shaders
from ursina.prefabs.primitives import WhiteCube, WhiteSphere, GrayPlane

if __name__ == "__main__":
    app = Ursina()
    window.color = color.black
    shader = shaders.basic_lighting_shader
    a = WhiteCube(shader=shaders.basic_lighting_shader)
    b = WhiteSphere(shader=shaders.basic_lighting_shader, x=3)
    GrayPlane(scale=10, y=-2, texture="shore", shader=shaders.basic_lighting_shader)
    Sky(color=color.light_gray)
    EditorCamera()

    def update():
        b.rotation_y += 1
        b.rotation_x += 1
        b.set_shader_input("transform_matrix", b.getNetTransform().getMat())

    app.run()
