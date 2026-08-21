from ursina import Ursina, window, color, Animation, camera, application

app = Ursina()
window.color = color.white

deno = Animation("dino", collider="box", x=-5)

camera.orthographic = True
camera.fov = 10


def input(key):
    if key == 'escape':
        application.quit()


app.run()
