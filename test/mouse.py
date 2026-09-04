from ursina import Ursina, Button, mouse, scene

if __name__ == "__main__":
    app = Ursina()
    Button(parent=scene, text="a")

    def input(key):
        if key == "space":
            mouse.locked = not mouse.locked
            print(mouse.velocity)

    app.run()
