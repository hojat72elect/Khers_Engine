from ursina import Button, Ursina, window, NineSlice, color, hsv, Entity, camera
from ursina.prefabs.options_menu import OptionsMenu

if __name__ == "__main__":
    app = Ursina()
    window.color = hsv(0, 0, 10 / 255)
    Button.default_color = color._24
    Button.default_highlight_color = color._32
    NineSlice.outset = 0.4
    Button.default_color = color.white
    Button.default_model = NineSlice
    Button.default_texture = "nineslice_rainbow"
    Button.default_radius = 0.5
    options_menu = OptionsMenu()
    background = Entity(parent=camera.ui, model="quad", texture="shore", scale=(camera.aspect_ratio, 1), color=color.dark_gray, z=1, world_y=0)
    app.run()
