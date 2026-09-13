from ursina import Ursina, Entity, Quad, color, camera, curve, load_texture, EditorCamera, Vec2
from ursina.shaders.fresnel_shader import fresnel_shader

if __name__ == "__main__":
    app = Ursina()
    ball1 = Entity(model="sphere", color=color.black, shader=fresnel_shader)
    ball2 = Entity(model=Quad(), color=color.dark_gray, shader=fresnel_shader, x=0.25, parent=camera.ui, scale=0.2, ignore=True)
    ball2.shader_input = {
        "bias": 0.01,
        "scale": 1.5,
        "power": 1.5,
        "fresnel_color": color.hex("#123123"),
    }
    ball2.animate_rotation_y(15, duration=1, curve=curve.linear_boomerang, loop=True)
    ground = Entity(model="plane", color=color.gray, shader=fresnel_shader, y=-1, scale=64, texture="grass", texture_scale=Vec2(32, 32))
    ground.set_shader_input("fresnel_color", color.gray)
    ground.set_shader_input("fresnel_texture", load_texture("white_cube"))
    EditorCamera()
    app.run()
