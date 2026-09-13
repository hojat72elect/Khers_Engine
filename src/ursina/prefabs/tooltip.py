from ursina import *

class Tooltip(Text):

    def __init__(self, text='', wordwrap=40, background_color=color.black66, background_model_class=Quad, background_radius=.1, padding=.05, **kwargs):
        super().__init__(text=text, ignore=False, parent=camera.ui, wordwrap=wordwrap, origin=(-.5,-.5), margin=(2,2), enabled=False)

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.create_background(padding=padding, model_class=background_model_class, radius=background_radius, color=background_color)
        self._width = self.width



    def update(self):
        self.position = mouse.position
        self.position = (
            mouse.x + (self.margin[0] * self.size/2) + .01,
            mouse.y + (self.margin[1] * self.size/2) + .01
            )
        self.x = min(self.x, (.5 * window.aspect_ratio) - self._width - self.size - .005)
        self.y = min(self.y, .5 - (self.height + self.size + .005))
        self.z = -99
