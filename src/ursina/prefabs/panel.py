from ursina.entity import Entity
from ursina.models.procedural.quad import Quad
from ursina.prefabs.button import Button
from ursina import camera

class Panel(Entity):

    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.model = Quad()
        self.color = Button.default_color

        for key, value in kwargs.items():
            setattr(self, key, value)
