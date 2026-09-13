from ursina import Ursina, Entity, camera, Sky, EditorCamera, color, Vec3
from ursina.shaders.screenspace_shaders.camera_noise import camera_noise_shader
import random

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    camera.shader = camera_noise_shader
    EditorCamera()
    Sky()

    def update():
        # Since there isn't really a way to generate pseudorandom numbers in GLSL by themselves, this needs to be put here, otherwise the noise will be static.
        camera.set_shader_input("noise_offset", Vec3(*(random.randint(0, 100)/100 for _ in range(3))))

    app.run()
