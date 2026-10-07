from ursina import color
from ursina.prefabs.button import Button
from ursina.window import instance as window
from ursina.text import Text

window.fullscreen = True
window.color = color.black
Text.size *= 2
Button.default_color = color.azure
color.text_color = color.orange
