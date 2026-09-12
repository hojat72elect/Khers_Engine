from ursina import *
from ursina.shaders import unlit_shader

class Sky(Entity):
    default_values = dict(parent=camera, name='sky', model='sky_dome', texture='sky_default', scale=9900, shader=unlit_shader, unlit=True)
    instances = []

    def __init__(self, **kwargs):
        super().__init__(**(__class__.default_values | kwargs))

        # self.setDepthWrite(False)
        __class__.instances.append(self)
        self.setBin('background', 0)


    def update(self):
        self.world_rotation = Vec3(0,0,0)
        self.scale = camera.clip_plane_far * .8
