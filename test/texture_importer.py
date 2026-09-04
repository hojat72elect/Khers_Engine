from ursina import Ursina, Entity

if __name__ == "__main__":
    app = Ursina()
    Entity(model="quad", texture="white_cube")
    app.run()
