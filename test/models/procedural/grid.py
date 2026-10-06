from ursina import Ursina, Grid
from ursina.entity import Entity

if __name__ == '__main__':
    app = Ursina()
    Entity(model=Grid(2, 6))
    app.run()
