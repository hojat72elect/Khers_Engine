from ursina import Button, Entity, Quad, Ursina, color, grid_layout

if __name__ == "__main__":
    app = Ursina()
    p = Entity(x=-2)

    for key in color.colors:
        print(key)
        b = Button(parent=p, model=Quad(0), color=color.colors[key], text=key)
        b.text_entity.scale *= 0.5

    grid_layout(p.children, max_x=8)

    for name in ("r", "g", "b", "h", "s", "v", "brightness"):
        print(name + ":", getattr(color.random_color(), name))

    e = Entity(model="cube", color=color.lime)
    print(e.color.name)
    print("rgb to hex:", color.rgb_to_hex(*color.blue))
    e.color = color.rgba32(1, 2, 3)
    app.run()
