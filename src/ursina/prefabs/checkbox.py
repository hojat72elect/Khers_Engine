from ursina import Button, Quad
from ursina.text import Text

class Checkbox(Button):
    def __init__(self, start_value=False, **kwargs):
        super().__init__(scale=Text.size, model=Quad(radius=.25))
        self.start_value = start_value
        self.value = start_value
        for key, value in kwargs.items():
            setattr(self, key, value)

    def on_click(self):
        self.value = not self.value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.text = ' x'[int(new_value)]
