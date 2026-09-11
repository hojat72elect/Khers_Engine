from ursina import Draggable, EditorCamera, Entity, Sky, Slider, Ursina, color, load_texture, scene, window, Vec2, Vec3
from ursina.shaders.triplanar_shader import triplanar_shader

if __name__ == "__main__":
    app = Ursina()
    window.color = color.black
    shader = triplanar_shader
    a = Draggable(parent=scene, model="cube", shader=shader, texture=load_texture("brick"), plane_direction=Vec3(0, 1, 0))
    t = load_texture("brick")._texture
    print("------", type(t))
    a.set_shader_input("side_texture", load_texture("brick"))
    b = Entity(model="sphere", shader=shader, color=color.azure, rotation_y=180, x=3, texture="grass")
    b.texture.filtering = False
    Entity(model="plane", color=color.gray, scale=10, y=-2, texture="shore")
    b.set_shader_input("side_texture", load_texture("brick"))
    Sky(color=color.light_gray)
    EditorCamera()

    def set_side_texture_scale():
        value = side_texture_scale_slider.value
        b.set_shader_input("side_texture_scale", Vec2(value, value))
        a.set_shader_input("side_texture_scale", Vec2(value, value))

    side_texture_scale_slider = Slider(text="side_texture_scale", min=0, max=10, default=1, dynamic=True, on_value_changed=set_side_texture_scale)

    def update():
        b.rotation_y += 1
        b.rotation_x += 1

    app.run()
