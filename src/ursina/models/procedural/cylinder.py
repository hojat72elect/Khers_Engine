from ursina import *

class Cylinder(Pipe):
    def __init__(self, resolution=8, radius=.5, start=0, height=1, direction=(0,1,0), mode='triangle', **kwargs):
        super().__init__(
            base_shape=Circle(resolution=resolution, radius=.5),
            origin=(0,0),
            path=((0,start,0), Vec3(direction) * (height+start)),
            thicknesses=((radius*2, radius*2),),
            mode=mode,
            **kwargs
            )
