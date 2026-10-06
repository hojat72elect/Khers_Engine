from ursina import TextureScroller, Ursina
from ursina.entity import Entity
from ursina.vec2 import Vec2

if __name__ == "__main__":
    app = Ursina()
    p = Entity(model="quad", texture="brick")
    p.add_script(TextureScroller(speed=Vec2(1, 1)))
    app.run()
