from ursina import Ursina, camera, Entity, time, application

app = Ursina()

camera.orthographic = True
camera.fov = 8

snake = Entity(model="cube", texture="snake", scale=0.4, z=-1, collider="box")
body = [Entity(model="cube", scale=0.2, texture="body") for i in range(25)]

dx = dy = 0


def update():
    for i in range(len(body) - 1, 0, -1):
        pos = body[i - 1].position
        body[i].position = pos
    body[0].x = snake.x
    body[0].y = snake.y
    snake.x += time.dt * dx
    snake.y += time.dt * dy


def input(key):
    global dx, dy
    if key == 'escape':
        application.quit()
    for x, y, z in zip(["d", "a"], [2, -2], [270, 90]):
        if key == x:
            snake.rotation_z = z
            dx = y
            dy = 0
    for x, y, z in zip(["w", "s"], [2, -2], [180, 0]):
        if key == x:
            snake.rotation_z = z
            dy = y
            dx = 0


app.run()
