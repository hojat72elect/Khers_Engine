from ursina import Ursina, Animation, Sky, camera, application, Entity, held_keys, time, curve, invoke, destroy, duplicate

app = Ursina()

me = Animation("player", collider="box", y=5)
Sky()

camera.orthographic = True
camera.fov = 20

Entity(model="quad", texture="BG", scale=36, z=1)
fly = Entity(model="cube", texture="fly1", collider="box", scale=2, x=20, y=-10)
flies = []


def newFly():
    new = duplicate(fly, y=-5 + (5124 * time.dt) % 15)
    flies.append(new)
    invoke(newFly, delay=1)


newFly()


def input(key):
    if key == 'escape':
        application.quit()
    if key == "space":
        e = Entity(y=me.y, x=me.x + 2, model="cube", texture="Bullet", collider="box")
        e.animate_x(30, duration=2, curve=curve.linear)
        invoke(destroy, e, delay=2)


def update():
    for fly in flies:
        fly.x -= 4 * time.dt
    me.y += held_keys["w"] * 6 * time.dt
    me.y -= held_keys["s"] * 6 * time.dt
    a = held_keys["w"] * -20
    b = held_keys["s"] * 20
    if a != 0:
        me.rotation_z = a
    else:
        me.rotation_z = b


app.run()
