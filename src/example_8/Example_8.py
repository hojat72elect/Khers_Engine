from ursina import Ursina, Sky, Entity
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
Sky()
ground = Entity(model="plane", texture="grass", collider="mesh", scale=(100, 1, 100))
player = FirstPersonController(position=(0, 2, -5))


def input(key):
    if key == 'escape':
        app.quit()


app.run()
