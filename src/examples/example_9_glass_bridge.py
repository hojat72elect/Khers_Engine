from random import randint

from ursina import Ursina, Entity, application, color, duplicate, invoke, destroy
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController(collider="box")
ground = Entity(model="plane", texture="grass", collider="mesh", scale=(30, 0, 3))

pill1 = Entity(model="cube", color=color.violet, scale=(0.4, 0.1, 53), z=28, x=-0.7)
pill2 = duplicate(pill1, x=-3.7)
pill3 = duplicate(pill1, x=0.6)
pill4 = duplicate(pill1, x=3.6)

blocks = []
for i in range(12):
    block = Entity(model="cube", collider="box", color=color.white33, position=(2, 0.1, 3 + i * 4), scale=(3, 0.1, 2.5))
    block2 = duplicate(block, x=-2.2)

    blocks.append((block, block2, randint(0, 3) > 0, randint(0, 3) > 0))

goal = Entity(model="cube", collider="mesh", texture="grass", scale=(10, 1, 10), z=55)
pillar = Entity(model="cube", color=color.brown, scale=(1, 15, 1), y=8, z=58)


def input(key):
    if key == 'escape':
        application.quit()


def update():
    for block1, block2, k, n in blocks:
        for x, y in [(block1, k), (block2, n)]:
            if x.intersects() and y:
                invoke(destroy, x, delay=0.1)
                x.fade_out(duration=0.1)


app.run()
