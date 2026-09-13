from ursina import Ursina, Entity, Vec3, scene, Sky, color, EditorCamera, held_keys, time
from ursina.shaders.lit_with_shadows_shader import lit_with_shadows_shader
from ursina.lights import DirectionalLight

if __name__ == "__main__":
    app = Ursina()
    shader = lit_with_shadows_shader
    a = Entity(model="cube", shader=shader, y=1, color=color.light_gray)
    Entity(model="sphere", texture="shore", y=2, x=1, shader=shader)
    Entity(model="plane", scale=16, texture="grass", shader=lit_with_shadows_shader)
    sun = DirectionalLight(shadow_map_resolution=(2048, 2048))
    sun.look_at(Vec3(-1, -1, -10))
    scene.fog_density = (10, 500)
    scene.fog_color = color.blue
    Sky(color=color.light_gray)
    EditorCamera()

    def update():
        a.x += (held_keys["d"] - held_keys["a"]) * time.dt * 5
        a.y += (held_keys["e"] - held_keys["q"]) * time.dt * 5
        a.z += (held_keys["w"] - held_keys["s"]) * time.dt * 5

    def input(key):
        if key == "r":
            if sun.color == color.white:
                sun.color = color.red
            else:
                sun.color = color.white

    app.run()
