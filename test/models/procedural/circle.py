from ursina import Ursina, Entity, color, EditorCamera, Circle

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model=Circle(8, mode="line", thickness=10), color=color.hsv(60, 1, 1, 0.3))
    e = Entity(model=Circle(8, mode="line", thickness=10), color=color.hsv(60, 1, 1, 0.3), x=1)
    print(e.model)
    origin = Entity(model="quad", color=color.orange, scale=(0.05, 0.05))
    ed = EditorCamera(rotation_speed=200, panning_speed=200)
    app.run()
