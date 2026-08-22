from ursina import Ursina, window, color, Animation, camera, application, Entity

app = Ursina()
window.color = color.white

deno = Animation("dino", collider="box", x=-5)
ground1 = Entity(model="quad", texture="ground", scale=(50, 0.5, 1), z=1)

camera.orthographic = True
camera.fov = 10


def input(key):
    if key == 'escape':
        application.quit()


app.run()
