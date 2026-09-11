from ursina import Ursina, window, color, Sky, EditorCamera
from ursina.prefabs.primitives import GrayPlane, AzureSphere
from ursina.shaders.geom_shader import point_shader

if __name__ == "__main__":
    app = Ursina(vsync=False)
    window.color = color.black

    b = AzureSphere(rotation_y=180, x=3, scale=2)
    b.model.mode = "point"
    b.model.colors = [color.random_color() for e in b.model.vertices]
    b.model.generate()
    b.shader = point_shader
    GrayPlane(scale=10, y=-2, texture="shore")

    Sky(color=color.light_gray)
    EditorCamera()
    app.run()
