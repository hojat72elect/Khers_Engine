from ursina import EditorCamera, Entity, Plane, Ursina, color, duplicate

if __name__ == "__main__":
    app = Ursina()
    front = Entity(model=Plane(subdivisions=(3, 6)), texture="brick", rotation_x=-90)
    wireframe_renderer = duplicate(front, wireframe=True, color=color.azure, always_on_top=True)
    _ed = EditorCamera()
    Entity(model="cube", color=color.green, scale=0.05)
    app.run()
