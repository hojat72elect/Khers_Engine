from ursina import Ursina, Entity, EditorCamera, held_keys, color
from ursina.shaders.toon_shader import toon_shader

if __name__ == "__main__":
    app = Ursina()
    shader = toon_shader
    e = Entity(model="sphere", y=2, color=color.azure, shader=shader)
    e.model.generate_normals(smooth=True)
    Entity(model="plane", scale=8, shader=shader)
    EditorCamera()

    def update():
        if held_keys["d"]:
            e.rotation_y += 4
        if held_keys["a"]:
            e.rotation_y -= 4

    app.run()
