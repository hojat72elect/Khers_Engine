from ursina import Ursina, Draggable, scene, Vec3, Entity, Cone, color, Grid, held_keys, time, EditorCamera

if __name__ == '__main__':
    app = Ursina()

    draggable = Draggable(parent=scene, model="cube", plane_direction=Vec3.up)
    turret = Entity(model=Cone(), scale=Vec3(0.5, 1, 0.5), origin_y=-0.5, color=color.azure)
    turret.model.colorize()
    grid = Entity(model=Grid(8, 8), scale=8, rotation_x=90)

    def update():
        turret.lookAt(draggable.position, Vec3.up)
        draggable.y += (held_keys['e'] - held_keys['q']) * time.dt * 10

    EditorCamera()
    app.run()
