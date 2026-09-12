from ursina import *

class TextureScroller:
    def __init__(self, speed:Vec2=None):
        self.speed = speed or Vec2(.005,.005)

    def update(self):
        self.entity.texture_offset += self.speed * time.dt
