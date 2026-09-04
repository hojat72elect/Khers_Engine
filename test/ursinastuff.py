from ursina import Ursina, Audio, destroy

if __name__ == '__main__':
    app = Ursina()

    a = Audio("sine")
    a.play()
    destroy(a, delay=1)

    app.run()