from ursina import Ursina, Entity, curve, EditorCamera, DirectionalLight, application, color

app = Ursina()
DirectionalLight(y=2, z=-3)
cube = Entity(model="cube", color=color.hsv(490, 4, 1), scale=2, collider="box", texture="white_cube")

def spin():
    cube.animate("rotation_y", cube.rotation_y + 360, duration=6, curve=curve.out_cubic)

cube.on_click = spin
EditorCamera()

def input(key):
    if key == 'escape':
        application.quit()

app.run()
