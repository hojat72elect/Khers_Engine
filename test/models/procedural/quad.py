from ursina import Entity, Quad, Ursina, camera, color

if __name__ == "__main__":
    app = Ursina()
    from time import perf_counter
    t = perf_counter()

    for i in range(100):
        Entity(model=Quad(scale=(3, 1), thickness=3, segments=3, mode="line"), color=color.hsv(0, 1, 1, 0.7))

    origin = Entity(model="quad", color=color.orange, scale=(0.05, 0.05))
    Entity(model=Quad(0), texture="shore", x=-1)
    camera.z = -5
    app.run()
