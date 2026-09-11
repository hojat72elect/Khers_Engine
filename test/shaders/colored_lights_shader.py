from ursina import EditorCamera, Entity, Sky, Ursina, color, hsv, shaders, window
from ursina.prefabs.primitives import GrayPlane

if __name__ == "__main__":
    app = Ursina()
    window.color = color.black
    shader = shaders.colored_lights_shader

    Entity(model="cube", shader=shaders.colored_lights_shader)
    e = Entity(model="cube", x=1.2, shader=shaders.colored_lights_shader)
    e.set_shader_input("top_color", hsv(0, 1, 1))
    e.set_shader_input("bottom_color", hsv(0, 0, 0))
    e.set_shader_input("left_color", hsv(0, 0, 0))
    e.set_shader_input("right_color", hsv(0, 0, 0))
    e.set_shader_input("front_color", hsv(0, 0, 0))
    e.set_shader_input("back_color", hsv(0, 0, 0))

    GrayPlane(scale=10, y=-2, texture="shore")
    Sky(color=color.light_gray)
    EditorCamera()
    app.run()
