from ursina import Vec3, lerp_exponential_decay, time

class SmoothFollow:
    def __init__(self, target=None, offset=Vec3.zero, speed=8, rotation_speed=0, rotation_offset=Vec3.zero):
        self.target = target
        self.offset = Vec3(*offset)
        self.speed = speed
        self.rotation_speed = rotation_speed
        self.rotation_offset = rotation_offset

    def update(self):
        if not self.target:
            return

        self.entity.world_position = lerp_exponential_decay(self.entity.world_position, self.target.world_position+self.offset, time.dt*self.speed)

        if self.rotation_speed > 0:
            self.entity.world_rotation = lerp_exponential_decay(self.entity.world_rotation, self.target.world_rotation+self.rotation_offset, time.dt*self.rotation_speed)
