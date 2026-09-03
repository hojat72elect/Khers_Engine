from random import uniform
from ursina import Button, scene, color

class Voxel(Button):
    """
    Our voxel is just a 3D button, with a "cube" model and a "scene" parent.
    """
    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model="cube",
            origin_y=0.5,
            texture="white_cube",
            color=color.hsv(0, 0, uniform(0.9, 1.0)),
            highlight_color=color.lime
        )
