from ursina import Entity, color


class Player():
    def __init__(self, ground_entity: Entity):
        self.entity = Entity(model='quad', color=color.rgb(50, 225, 30), scale=(1.5, 1.5), position=(-8, ground_entity.y + ground_entity.scale_y / 2 + 0.75))
        self.vertical_velocity = 0
        self.is_jumping = False
