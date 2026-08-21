from ursina import Ursina, application, Entity, camera

app = Ursina()

background = Entity(model="quad", texture="BG2", scale=55, z=10, y=15)
player = Entity(model="quad", collider="box", texture="square")

camera.orthographic = True
camera.fov = 18


def input(key):
    if key == 'escape':
        application.quit()


app.run()
