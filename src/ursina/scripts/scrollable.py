from ursina import *

class Scrollable:

    def __init__(self, **kwargs):
        super().__init__()
        self.max = inf
        self.min = -inf
        self.scroll_speed = .05
        self.scroll_smoothing = 16
        self.axis = 'y'
        self.target_value = None

        for key, value in kwargs.items():
            setattr(self, key, value)



    def update(self):
        # lerp position
        if self.target_value:
            setattr(self.entity, self.axis, lerp(getattr(self.entity, self.axis), self.target_value, time.dt * self.scroll_smoothing))



    def input(self, key):
        if not mouse.hovered_entity:
            return

        if not self.target_value:
            self.target_value = getattr(self.entity, self.axis)

        if self.entity.hovered or mouse.hovered_entity.has_ancestor(self.entity):
            # print(key)
            if key == 'scroll up':
                self.target_value -= self.scroll_speed
            if key == 'scroll down':
                self.target_value += self.scroll_speed


            self.target_value = max(min(self.target_value, self.max), self.min)
