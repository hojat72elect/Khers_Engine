from ursina import Ursina, Sky, Button, color, scene, application
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
Sky(texture="sky_sunset")
player = FirstPersonController()

boxes = []
for n in range(12):
    for k in range(12):
        box = Button(color=color.white, model="cube", position=(k, 0, n), texture="grass", parent=scene, origin_y=0.5)
        boxes.append(box)


def input(key):
    if key == 'escape':
        application.quit()


app.run()
