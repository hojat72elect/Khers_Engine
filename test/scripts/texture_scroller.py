from ursina import Entity, TextureScroller, Ursina, Vec2

if __name__ == "__main__":
    app = Ursina()
    p = Entity(model="quad", texture="brick")
    p.add_script(TextureScroller(speed=Vec2(1, 1)))
    app.run()
