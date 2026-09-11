from ursina import Ursina, window, color, Entity, hsv, time, Sprite
from ursina.shaders.noise_fog_shader import noise_fog_shader

if __name__ == "__main__":
    app = Ursina()
    window.color = color.black
    e = Entity(model="quad", texture="perlin_noise", shader=noise_fog_shader, scale=6)
    e.set_shader_input("dark_color", hsv(280, 1, 0.1, 0))
    e.set_shader_input("light_color", color.cyan)
    app.t = 0

    def update():
        app.t += time.dt
        e.set_shader_input("time", app.t)

    bg = Sprite("shore", scale=1, z=1, color=color.dark_gray)
    window.size *= 0.5
    app.run()
