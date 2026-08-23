from random import randint

from ursina import Ursina, Sky, Animation, color, camera, SmoothFollow, application, held_keys, time, Entity, duplicate, curve, destroy

app = Ursina()
Sky()

bird = Animation("bird", collider="box", color=color.orange, y=15)
camera.add_script(SmoothFollow(target=bird, offset=[0, 0, -40], speed=6))

platform = Entity(model="cube", color=color.green, texture="white_cube", collider="box", scale=(3, 0.5))
plates = []
for i in range(5):
    p = duplicate(platform, y=platform.y + 5)
    plates.append(p)


def input(key):
    if key == 'escape':
        application.quit()


def update():
    bird.x -= held_keys["a"] * 12 * time.dt
    bird.x += held_keys["d"] * 12 * time.dt
    bird.y -= 7 * time.dt
    if bird.intersects().hit:
        bird.animate_y(bird.y + 7, duration=0.3, curve=curve.in_circ)
        plates.append(duplicate(platform, y=plates[-1].y + 5, x=randint(-5, 5)))
        obj = plates[0]
        plates.pop(0)
        destroy(obj)


app.run()
