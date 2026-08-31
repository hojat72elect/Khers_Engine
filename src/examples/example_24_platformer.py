from random import seed, randint

from ursina import Ursina, window, color, camera, Entity, raycast, SmoothFollow, input_handler, application
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

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

input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'space')
input_handler.bind('gamepad dpad right', 'd')
input_handler.bind('gamepad dpad left', 'a')
input_handler.bind('gamepad a', 'space')

if application.development_mode:
    from ursina.scripts.noclip_mode import NoclipMode2d

    player.add_script(NoclipMode2d())

app.run()
