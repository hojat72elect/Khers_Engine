from ursina import Ursina, Sky, Button, color, scene, application, Entity, camera, held_keys
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
Sky(texture="sky_sunset")
player = FirstPersonController()

boxes = []
for n in range(12):
    for k in range(12):
        box = Button(color=color.white, model="cube", position=(k, 0, n), texture="grass", parent=scene, origin_y=0.5)
        boxes.append(box)

sword = Entity(model="blade", texture="sword", rotation=(30, -40), position=(0.5, -0.6), parent=camera.ui, scale=(0.2, 0.15))


def input(key):
    if key == 'escape':
        application.quit()


def update():
    if held_keys["left mouse"]:
        sword.position = (0.4, -0.5)
    elif held_keys["right mouse"]:
        sword.position = (0.4, -0.5)
    else:
        sword.position = (0.5, -0.6)


app.run()
