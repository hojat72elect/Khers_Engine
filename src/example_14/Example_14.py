from ursina import Ursina, camera, Entity, application, held_keys, time

app = Ursina()

camera.orthographic = True
camera.fov = 10

car = Entity(model="quad", texture="car", collider="box", scale=(2, 1), rotation_z=-90)


def update():
    car.x -= held_keys["a"] * 5 * time.dt
    car.x += held_keys["d"] * 5 * time.dt


def input(key):
    if key == 'escape':
        application.quit()


app.run()
