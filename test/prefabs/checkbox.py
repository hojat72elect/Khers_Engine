from ursina import Checkbox, Slider, Ursina

if __name__ == "__main__":
    app = Ursina()
    Checkbox(start_value=True)
    Checkbox(x=0.1, start_value=False)
    Slider(y=-0.1)
    app.run()
