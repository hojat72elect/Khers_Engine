from ursina import Ursina, Animation, Sky, camera, application, Entity, held_keys, time

app = Ursina()

me = Animation("player", collider="box", y=5)
Sky()

camera.orthographic = True
camera.fov = 20

Entity(model="quad", texture="BG", scale=36, z=1)


def input(key):
    if key == 'escape':
        application.quit()


def update():
    me.y += held_keys["w"] * 6 * time.dt
    me.y -= held_keys["s"] * 6 * time.dt
    a = held_keys["w"] * -20
    b = held_keys["s"] * 20
    if a != 0:
        me.rotation_z = a
    else:
        me.rotation_z = b


app.run()
