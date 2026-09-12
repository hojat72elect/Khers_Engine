from ursina import Ursina, color, Button, scene, EditorCamera
from ursina.prefabs.radial_menu import RadialMenu, RadialMenuButton

if __name__ == '__main__':
    app = Ursina()
    rm = RadialMenu(
        buttons=(
            RadialMenuButton(text="1"),
            RadialMenuButton(text="2"),
            RadialMenuButton(text="3"),
            RadialMenuButton(text="4"),
            RadialMenuButton(text="5", scale=0.5),
            RadialMenuButton(text="6", color=color.red),
        ),
        enabled=False,
    )
    RadialMenuButton(text='6', color=color.red,x =-.5, scale=.06)

    def enable_radial_menu():
        rm.enabled = True

    cube = Button(parent=scene, model='cube', color=color.orange, highlight_color=color.azure, on_click=enable_radial_menu)
    EditorCamera()
    app.run()
