from ursina import Ursina
from ursina.prefabs.gradient_editor import GradientEditor

if __name__ == '__main__':
    app = Ursina()
    GradientEditor()
    app.run()