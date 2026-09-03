from typing import Final
from ursina import Entity, color, Text, Audio, Ursina, held_keys, time, mouse

class Example1:
    MOVEMENT_SPEED: Final[int] = 5

    def __init__(self):
        self.app = Ursina()

        self.background = Entity(model='quad', scale=(16, 16), color=color.white, z=1)
        self.potato = Entity(model='quad', texture='assets/potato.png', scale=(0.5, 0.5), position=(-5, 0, 0), collider='box')
        self.target_section = Entity(model='quad', scale=(4, 7), position=(2, 2, 0), color=color.black, collider='box')
        self.hello_text = Text(text='Hello World!', position=(0.0, 0.15), origin=(0, 0), color=color.black, scale=1.5)
        self.clank_sound = Audio('assets/clank.wav', autoplay=False)
        self.is_potato_colliding = False
        self.is_mouse_hovering: bool = False

    def listenToInputs(self):
        if held_keys['d']:
            self.potato.x += Example1.MOVEMENT_SPEED * time.dt
        if held_keys['a']:
            self.potato.x -= Example1.MOVEMENT_SPEED * time.dt
        if held_keys['w']:
            self.potato.y += Example1.MOVEMENT_SPEED * time.dt
        if held_keys['s']:
            self.potato.y -= Example1.MOVEMENT_SPEED * time.dt

    def handleCollisions(self):
        collision_info = self.potato.intersects(self.target_section)
        self.is_potato_colliding = collision_info.hit
        self.is_mouse_hovering = mouse.hovered_entity == self.target_section

        if self.is_potato_colliding and self.is_mouse_hovering:
            self.target_section.color = color.yellow
        elif self.is_potato_colliding:
            self.target_section.color = color.red
        elif self.is_mouse_hovering:
            self.target_section.color = color.blue
        else:
            self.target_section.color = color.black

    def run(self):
        self.app.run()
