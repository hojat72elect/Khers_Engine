from ursina import Ursina, camera, Entity, color, EditorCamera, SmoothFollow
from ursina.prefabs.platformer_controller_2d import PlatformerController2d

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 10
    ground = Entity(model='cube', color=color.white33, origin_y=.5, scale=(20, 1, 1), collider='box', y=-1)
    wall = Entity(model='cube', color=color.azure, origin=(-.5,.5), scale=(5,10), x=10, y=.5, collider='box')
    wall_2 = Entity(model='cube', color=color.white33, origin=(-.5,.5), scale=(5,10), x=10, y=0, collider='box')
    ceiling = Entity(model='cube', color=color.white33, origin_y=-.5, scale=(1, 1, 1), y=1, collider='box')
    ceiling = Entity(model='cube', color=color.white33, origin_y=-.5, scale=(5, 5, 1), y=2, collider='box')
    ground = Entity(model='cube', color=color.white33, origin_y=.5, scale=(20, 3, 1), collider='box', y=-1, rotation_z=45, x=-5)

    def input(key):
        if key == 'c':
            wall.collision = not wall.collision
            print(wall.collision)

    player_controller = PlatformerController2d(scale_y=2, jump_height=4, x=3, y=20, max_jumps=2)
    ec = EditorCamera()
    ec.add_script(SmoothFollow(target=player_controller, offset=[0,1,0], speed=4))
    app.run()
