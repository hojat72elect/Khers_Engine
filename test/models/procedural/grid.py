from ursina import Ursina, Entity, Grid

if __name__ == '__main__':
    app = Ursina()
    Entity(model=Grid(2, 6))
    app.run()
