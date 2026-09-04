from ursina import Audio, Ursina
import random

if __name__ == "__main__":
    app = Ursina()
    a = Audio("sine", loop=True, autoplay=True)

    a.volume = 0.5
    print("---", a.volume)

    def input(key):
        if key == "space":
            Audio("sine", pitch=random.uniform(0.5, 1), loop=True)

    app.run()
