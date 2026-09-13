from ursina import *

class TrailRenderer(Entity):
    def __init__(self, size=[1,.01], segments=8, min_spacing=.05, fade_speed=0, color_gradient=[color.white, color.clear], **kwargs):
        super().__init__(**kwargs)
        if color_gradient:
            color_gradient = color_gradient[::-1]

        self.renderer = Entity(
            model=Pipe(
                base_shape=Quad(segments=0, scale=size),
                path=[Vec3(0,0,i) for i in range(2)],
                color_gradient=color_gradient,
                static=False,
                cap_ends=False,
                look_at=True,
            ),
        )
        self._t = 0
        self.segments = segments
        self.update_step = .05
        self.min_spacing = min_spacing
        self.fade_speed = fade_speed

        self.on_enable = self.renderer.enable
        self.on_disable = self.renderer.disable


    def update(self):
        self._t += time.dt
        if self._t >= self.update_step:

            self._t = 0
            if distance(self.world_position, self.renderer.model.path[-1]) > self.min_spacing:
                self.renderer.model.path.append(self.world_position)
                if len(self.renderer.model.path) > self.segments:
                    self.renderer.model.path.pop(0)

            if self.fade_speed:
                for i, v in enumerate(self.renderer.model.path):
                    if i >= len(self.renderer.model.path)-1:
                        continue
                    self.renderer.model.path[i] = lerp(v, self.renderer.model.path[i+1], time.dt*self.fade_speed)
            self.renderer.model.generate()


    def on_destroy(self):
        destroy(self.renderer)
