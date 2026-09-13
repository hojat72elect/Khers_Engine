from ursina import Ursina, Entity, color, window, EditorCamera, held_keys, scene, camera
import random
from ursina.shaders.fog_of_war_shader import fog_of_war_shader

if __name__ == "__main__":
    app = Ursina()
    window.color = color.black
    Entity.default_shader = fog_of_war_shader
    editor_camera = EditorCamera()
    ground = Entity(model="plane", collider="box", scale=64, texture="grass", texture_scale=(4, 4))

    for i in range(16):
        Entity(
            model="cube",
            origin_y=-0.5,
            scale=2,
            texture="brick",
            texture_scale=(1, 2),
            x=random.uniform(-8, 8),
            z=random.uniform(-8, 8) + 8,
            collider="box",
            scale_y=random.uniform(2, 3),
            color=color.hsv(0, 0, random.uniform(0.9, 1)),
        )

    light = Entity(model="sphere", unlit=True, scale=0.5, y=1)

    def update():
        light.x += held_keys["d"] - held_keys["a"]
        light.z += held_keys["w"] - held_keys["s"]

        for e in scene.entities:
            if hasattr(e, "shader") and e.shader == fog_of_war_shader:
                e.set_shader_input("light_position", light.world_position + camera.world_position)
                
    app.run()
