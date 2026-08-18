from ursina import Ursina, Entity, hsv, curve, EditorCamera, DirectionalLight

app = Ursina()

DirectionalLight(y=2, z=-3, shadows=True)

cube = Entity(model="cube", color=hsv(120, 1, 1), scale=2, collider="box", texture="white_cube")


def spin():
    cube.animate("rotation_y", cube.rotation_y + 360, duration=2, curve=curve.in_out_expo)


cube.on_click = spin
EditorCamera()

app.run()
