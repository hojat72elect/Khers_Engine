from ursina import Ursina, color
from ursina.destroy import destroy
from ursina.entity import Entity
from ursina.input_handler import bind

if __name__ == '__main__':
    app = Ursina(borderless=False)
    bind('z', 'w')  # 'z'-key will now be registered as 'w'-key
    bind('left mouse down', 'attack')  # 'left mouse down'-key will now send 'attack'to input functions
    bind('gamepad b', 'attack')  # 'gamepad b'-key will now be registered as 'attack'-key

    def input(key):
        print("got key:", key)
        if key == "attack":
            destroy(Entity(model="cube", color=color.blue), delay=0.2)

    app.run()
