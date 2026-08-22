from random import randint

from ursina import Ursina, window, color, Animation, camera, application, Entity, duplicate, time, invoke, curve, Text

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
    if key == "space":
        if deno.y <= 0.1:
            deno.animate_y(2, duration=0.4, curve=curve.out_sine)
            invoke(deno.animate_y, 0, duration=0.4, curve=curve.in_sine, delay=0.4)


def update():
    global points
    points += 1
    label.text = f"Points: {points}"
    for groud in pair:
        groud.x -= 6 * time.dt
        if groud.x < -35:
            groud.x += 100
    for c in cacti:
        c.x -= 6 * time.dt
    if deno.intersects().hit:
        deno.texture = "hit"
        application.pause()


def newCactus():
    new = duplicate(cactus, x=10 + randint(0, 5))
    cacti.append(new)
    invoke(newCactus, delay=2)


newCactus()

label = Text(text=f"Points: {0}", color=color.black, position=(-0.6, 0.4))
points = 0

app.run()
