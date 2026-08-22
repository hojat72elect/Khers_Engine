from ursina import Ursina, window, color, Entity, camera, application, duplicate

app = Ursina()

window.color = color.olive
table = Entity(model="cube", color=color.black, scale=(2, 1, 3), rotation=(90, 0, 0))

ball = Entity(model="sphere", color=color.cyan, z=-1, scale=0.1, collider="box")
player1 = Entity(model="cube", color=color.cyan, scale=(0.6, 0.1, 1), position=(0, -1.4, -1), collider="box")
player2 = duplicate(player1, y=1.4)

camera.orthographic = True
camera.fov = 4


def input(key):
    if key == 'escape':
        application.quit()


app.run()
