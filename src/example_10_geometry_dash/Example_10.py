from ursina import Ursina, application, Entity, camera, color, time

app = Ursina()

background = Entity(model="quad", texture="BG2", scale=55, z=10, y=15)
player = Entity(model="quad", collider="box", texture="square")
ground = Entity(model="cube", color=color.yellow, y=-1, origin_y=.5, scale=(200, 15, 1), collider="box", texture="white_cube")

camera.orthographic = True
camera.fov = 18


def input(key):
    if key == 'escape':
        application.quit()


def update():
    if not player.intersects().hit:
        player.y -= time.dt
    player.y = max(-0.5, player.y)


app.run()
