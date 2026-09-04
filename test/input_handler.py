from ursina import Ursina, input_handler, destroy, Entity, color

if __name__ == '__main__':
    app = Ursina(borderless=False)
    input_handler.bind('z', 'w')  # 'z'-key will now be registered as 'w'-key
    input_handler.bind('left mouse down', 'attack')  # 'left mouse down'-key will now send 'attack'to input functions
    input_handler.bind('gamepad b', 'attack')  # 'gamepad b'-key will now be registered as 'attack'-key

    def input(key):
        print("got key:", key)
        if key == "attack":
            destroy(Entity(model="cube", color=color.blue), delay=0.2)

    app.run()
