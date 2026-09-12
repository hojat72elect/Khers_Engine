from ursina import Ursina, color, window, ButtonGroup, camera, Entity, Tooltip, Func, Button, Vec2

if __name__ == '__main__':
    app = Ursina()
    center = Entity(parent=camera.ui, model='circle', scale=.005, color=color.red, z=-1)
    gender_selection = ButtonGroup(("man", "woman", "other"), origin=(-0.5, 0), label="choose gender:", max_x=1)

    def on_value_changed():
        print('set gender:', gender_selection.value)
        
    gender_selection.on_value_changed = on_value_changed
    window.color = color._32

    for e in [(-.5,.5), (0,.5), (.5,.5), (-.5,0), (0,0), (.5,0), (-.5,-.5), (0,-.5), (.5,-.5)]:
        Button(text="*", model="quad", text_origin=e, scale=0.095, origin=(-0.5, 0.5), position=window.top_left + Vec2(*e) * 0.2 + Vec2(0.1, -0.1), tooltip=Tooltip(str(e)), on_click=Func(setattr, gender_selection, "origin", e))

    app.run()
