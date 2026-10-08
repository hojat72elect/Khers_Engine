from random import seed, randint
from ursina.raycast import raycast
from ursina.entity import Entity
from ursina.main import Ursina
from ursina.window import instance as window
from ursina.camera import instance as camera
from ursina.scripts.smooth_follow import SmoothFollow
from ursina import color, application
from ursina.input_handler import bind
from ursina.prefabs.platformer_controller_2d import PlatformerController2d
from ursina.scripts.noclip_mode import NoclipMode2d

app = Ursina()
window.color = color.light_gray
camera.orthographic = True
camera.fov = 20
ground = Entity(model="cube", color=color.olive.tint(-0.4), z=-0.1, y=-1, origin_y=0.5, scale=(1_000, 100, 10), collider="box", ignore=True)
seed(4)

for i in range(10):
    Entity(model="cube", color=color.dark_gray, collider="box", ignore=True, position=(randint(-20, 20), randint(0, 10)), scale=(randint(1, 20), randint(2, 5), 10))

player = PlatformerController2d()
player.x = 1
player.y = raycast(player.world_position, player.down).world_point[1] + 0.01
camera.add_script(SmoothFollow(target=player, offset=[0, 5, -30], speed=4))
bind('right arrow', 'd')
bind('left arrow', 'a')
bind('up arrow', 'space')
bind('gamepad dpad right', 'd')
bind('gamepad dpad left', 'a')
bind('gamepad a', 'space')

if application.development_mode:
    player.add_script(NoclipMode2d())

app.run()
