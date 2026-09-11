from ursina import Ursina, Entity, texture, load_texture, color, Texture, EditorCamera, mouse, held_keys, Vec3
from ursina.shaders.texture_blend_shader import texture_blend_shader

if __name__ == "__main__":
    Texture.default_filtering = "bilinear"
    app = Ursina(vsync=False)
    e = Entity(model="plane", shader=texture_blend_shader, texture="shore")
    e.set_shader_input("red_texture", load_texture("grass_tintable"))
    e.set_shader_input("red_tint", color.hex("#7e722e"))
    e.set_shader_input("green_texture", load_texture("grass_tintable.tif"))
    e.set_shader_input("green_tint", color.hex("#6f6d24"))
    e.set_shader_input("blue_texture", load_texture("cobblestone.tif"))
    blend_map = load_texture("blend_map_example")
    e.set_shader_input("blend_map", blend_map)
    e.scale_x = blend_map.width / blend_map.height
    e.scale *= 200
    EditorCamera(rotation_x=30)

    def input(key):
        if key == "space":
            if e.shader:
                e.shader = None
            else:
                e.shader = texture_blend_shader
        if key == "left mouse up":
            blend_map.apply()

    e.collider = "mesh"

    def update():
        if mouse.hovered_entity == e and mouse.left:
            x, _, y = mouse.point + Vec3(0.5)
            print(x, y)
            target_color = color.green
            if held_keys["control"]:
                target_color = color.red
            if held_keys["shift"]:
                target_color = color.blue

            blend_map.set_pixel(int(x * blend_map.width), int(y * blend_map.height), target_color)
            blend_map.apply()

    app.run()
