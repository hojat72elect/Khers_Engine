from ursina import Ursina, Animation, Sky, camera, application

app = Ursina()

me = Animation("player", collider="box", y=5)
Sky()

camera.orthographic = True
camera.fov = 20


def input(key):
    if key == 'escape':
        application.quit()


app.run()
