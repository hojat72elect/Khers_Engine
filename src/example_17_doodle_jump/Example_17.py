from ursina import Ursina, Sky, Animation, color, camera, SmoothFollow, application, held_keys, time

app = Ursina()
Sky()

bird = Animation("bird", collider="box", color=color.orange, y=15)
camera.add_script(SmoothFollow(target=bird, offset=[0, 0, -40], speed=6))

# platform =


def input(key):
    if key == 'escape':
        application.quit()


def update():
    bird.x -= held_keys["a"] * 12 * time.dt
    bird.x += held_keys["d"] * 12 * time.dt


app.run()
