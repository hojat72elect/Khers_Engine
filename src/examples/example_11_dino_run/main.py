from random import randint
from ursina import Ursina, window, color, Animation, camera, application, Entity, duplicate, time, invoke, curve, Text, Audio

app = Ursina()
window.color = color.white

dino = Animation("assets/dino", collider="box", x=-5)
ground1 = Entity(model="quad", texture="assets/ground", scale=(50, 0.5, 1), z=1)
ground2 = duplicate(ground1, x=50)
pair = [ground1, ground2]
cactus = Entity(model="quad", texture="assets/cacti", x=20, collider="box")
cacti = []
camera.orthographic = True
camera.fov = 10
sound = Audio("assets/beep", autoplay=False)

def input(key):
    if key == 'escape':
        application.quit()
    if key == "space":
        if dino.y <= 0.1:
            sound.play()
            dino.animate_y(2, duration=0.4, curve=curve.out_sine)
            invoke(dino.animate_y, 0, duration=0.4, curve=curve.in_sine, delay=0.4)

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
    if dino.intersects().hit:
        dino.texture = "hit"
        application.pause()

def newCactus():
    new = duplicate(cactus, x=10 + randint(0, 5))
    cacti.append(new)
    invoke(newCactus, delay=2)

newCactus()
label = Text(text=f"Points: {0}", color=color.black, position=(-0.6, 0.4))
points = 0
app.run()
