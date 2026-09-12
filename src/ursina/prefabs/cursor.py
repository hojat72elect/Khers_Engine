from ursina import Entity, Vec3, camera, color, mouse

class Cursor(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.texture = 'cursor'
        self.model = 'quad'
        self.color = color.light_gray
        # self.origin = (-.49, .49)
        self.scale *= .05
        self.render_queue = 1

        for key, value in kwargs.items():
            setattr(self, key, value)


    def update(self):
        self.position = Vec3(mouse.x, mouse.y, -100)
