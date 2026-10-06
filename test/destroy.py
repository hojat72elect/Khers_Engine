from ursina import Ursina
from ursina.destroy import destroy
from ursina.entity import Entity

if __name__ == '__main__':
    class E(Entity):
        def __init__(self, name):
            super().__init__()
            self.num_frames = 0
            self.name = name

        def update(self):
            self.num_frames += 1
            print(f"updating {self}")
            if self.name == "e2" and self.num_frames == 3:
                print("destroying e2")
                destroy(self)

    app = Ursina(window_type="none")
    e1 = E("e1")
    e2 = E("e2")
    e3 = E("e3")
    app.run()