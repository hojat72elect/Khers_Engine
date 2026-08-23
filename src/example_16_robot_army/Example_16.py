from ursina import Ursina, Entity, application, FrameAnimation3d, color, Sky
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()
ground = Entity(model="plane", texture="grass", collider="mesh", scale=(100, 1, 100))

robot = FrameAnimation3d("robot", position=(2, 0, 2), fps=18, scale=0.015, color=color.white66)
Sky()


def input(key):
    if key == 'escape':
        application.quit()


app.run()
