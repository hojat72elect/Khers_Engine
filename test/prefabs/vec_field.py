from ursina import Ursina, Sprite, color,Vec4
from ursina.prefabs.vec_field import VecField

if __name__ == '__main__':
    app = Ursina()

    def on_value_changed():
        print('set value to:', field.value)

    field = VecField(text=' int list', default_value=[10,1])
    field = VecField(text=' float list', default_value=[1.0,-2.0], y=-.1)
    field = VecField(text=' Vec4', default_value=Vec4(1,-2,0,0), y=-.2)
    field = VecField(text=' float', default_value=1.0, y=-.3)
    field = VecField(text=' int', default_value=0, y=-.4)
    Sprite('shore', color=color.dark_gray)
    app.run()
