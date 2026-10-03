from ursina import Ursina, destroy
from ursina.audio import Audio

if __name__ == '__main__':
    app = Ursina()
    a = Audio("sine")
    a.play()
    destroy(a, delay=1)
    app.run()