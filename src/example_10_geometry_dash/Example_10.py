from ursina import Ursina, application, Entity, camera, color, time, curve, duplicate, invoke

app = Ursina()

background = Entity(model="quad", texture="BG2", scale=55, z=10, y=15)
player = Entity(model="quad", collider="box", texture="square")
ground = Entity(model="cube", color=color.yellow, y=-1, origin_y=.5, scale=(200, 15, 1), collider="box", texture="white_cube")

camera.orthographic = True
camera.fov = 18

diam = []


def newObstacle(val):
    new1 = Entity(model="diamond", color=color.violet, y=-0.5, texture="white_cube", x=val, collider="mesh")
    new2 = duplicate(new1, y=0.35, x=val + 1, scale=0.8)
    diam.extend((new1, new2))
    invoke(newObstacle, val=val + 10, delay=1)


newObstacle(30)


def input(key):
    if key == 'escape':
        application.quit()
    if key == "space":
        if player.intersects().hit:
            player.animate_y(player.y + 3, duration=0.3, curve=curve.out_sine)
            player.animate_rotation_z(player.rotation_z + 180, duration=0.5, curve=curve.linear)


def update():
    for ob in diam:
        ob.x -= 10 * time.dt
    if not player.intersects().hit:
        player.y -= time.dt
    player.y = max(-0.5, player.y)


app.run()
