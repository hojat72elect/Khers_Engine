from ursina import Ursina, Sky, Animation, color, camera, SmoothFollow, application

app = Ursina()
Sky()

bird = Animation("bird", collider="box", color=color.orange, y=15)
camera.add_script(SmoothFollow(target=bird, offset=[0, 0, -40], speed=6))


def input(key):
    if key == 'escape':
        application.quit()

app.run()