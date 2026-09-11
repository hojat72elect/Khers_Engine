import random
from ursina import Entity, Sky, Ursina, application, camera
from ursina.shaders.sky_fade_shader import sky_fade_shader
from ursina.prefabs.first_person_controller import FirstPersonController

if __name__ == "__main__":
    app = Ursina()
    FirstPersonController(gravity=0)
    sky = Sky(texture="sky_sunset")
    e = Entity(model="plane", scale=(2000, 1, 2000), texture="grass", shader=sky_fade_shader)
    e.set_shader_input("sky_texture", sky.texture)

    for i in range(100):
        Entity(
            model="cube",
            scale=(25, random.randint(10, 150), 25),
            x=-1000 + (random.random() * 2000),
            z=-1000 + (random.random() * 2000),
            origin_y=-0.5,
            shader=sky_fade_shader,
            shader_input=dict(sky_texture=sky.texture)
        )
    print("-----------", camera.clip_plane_far)

    def input(key):
        if key == "escape":
            application.quit()

    app.run()
