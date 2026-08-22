from ursina import Ursina, camera, Entity, application, held_keys, time, duplicate

app = Ursina()

camera.orthographic = True
camera.fov = 10

car = Entity(model="quad", texture="car", collider="box", scale=(2, 1), rotation_z=-90)

road1 = Entity(model="quad", texture="road", scale=15, z=1)
road2 = duplicate(road1, y=15)
pair = [road1, road2]


def update():
    car.x -= held_keys["a"] * 5 * time.dt
    car.x += held_keys["d"] * 5 * time.dt
    for road in pair:
        road.y -= 6 * time.dt
        if road.y < -15:
            road.y += 30


def input(key):
    if key == 'escape':
        application.quit()


app.run()
