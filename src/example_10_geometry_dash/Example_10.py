from ursina import Ursina, application, Entity, camera, color, time, curve

app = Ursina()

background = Entity(model="quad", texture="BG2", scale=55, z=10, y=15)
player = Entity(model="quad", collider="box", texture="square")
ground = Entity(model="cube", color=color.yellow, y=-1, origin_y=.5, scale=(200, 15, 1), collider="box", texture="white_cube")

camera.orthographic = True
camera.fov = 18


def input(key):
    if key == 'escape':
        application.quit()
    if key == "space":
        if player.intersects().hit:
            player.animate_y(player.y + 3, duration=0.3, curve=curve.out_sine)
            player.animate_rotation_z(player.rotation_z + 180, duration=0.5, curve=curve.linear)


def update():
    if not player.intersects().hit:
        player.y -= time.dt
    player.y = max(-0.5, player.y)


app.run()
