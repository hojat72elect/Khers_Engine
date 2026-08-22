from random import randint

from ursina import Ursina, window, color, Animation, camera, application, Entity, duplicate, time, invoke

app = Ursina()
window.color = color.white

deno = Animation("dino", collider="box", x=-5)
ground1 = Entity(model="quad", texture="ground", scale=(50, 0.5, 1), z=1)
ground2 = duplicate(ground1, x=50)
pair = [ground1, ground2]

cactus = Entity(model="quad", texture="cacti", x=20, collider="box")
cacti = []

camera.orthographic = True
camera.fov = 10


def input(key):
    if key == 'escape':
        application.quit()


def update():
    for groud in pair:
        groud.x -= 6 * time.dt
        if groud.x < -35:
            groud.x += 100
    for c in cacti:
        c.x -= 6 * time.dt


def newCactus():
    new = duplicate(cactus, x=10 + randint(0, 5))
    cacti.append(new)
    invoke(newCactus, delay=2)


newCactus()

app.run()
