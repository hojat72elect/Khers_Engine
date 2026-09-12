from ursina import Ursina, Button, Entity, window, color, scene, camera, Vec3, duplicate, Func, destroy, curve, application
from ursina.prefabs.first_person_controller import FirstPersonController

if __name__ == '__main__':

    window.vsync = False
    app = Ursina()
    ground = Entity(model='plane', scale=(100,1,100), color=color.yellow.tint(-.2), texture='white_cube', texture_scale=(100,100), collider='box')
    e = Entity(model='cube', scale=(1,5,10), x=2, y=.01, rotation_y=45, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    e = Entity(model='cube', scale=(1,5,10), x=-2, y=.01, collider='box', texture='white_cube')
    e.texture_scale = (e.scale_z, e.scale_y)
    player = FirstPersonController(y=2, origin_y=-.5, height=1)
    player.gun = None
    gun = Button(parent=scene, model='cube', color=color.blue, origin_y=-.5, position=(3,0,3), collider='box', scale=(.2,.2,1))

    def get_gun():
        gun.parent = camera
        gun.position = Vec3(.5,0,.5)
        player.gun = gun

    gun.on_click = get_gun
    gun_2 = duplicate(gun, z=7, x=8)
    slope1 = Entity(model='cube', collider='box', position=(0,0,8), scale=6, rotation=(45,0,0), texture='brick', texture_scale=(8,8))
    slope2 = Entity(model='cube', collider='box', position=(5,0,10), scale=6, rotation=(80,0,0), texture='brick', texture_scale=(8,8))
    ceiling = Entity(model='cube', collider='box', position=(10,2,10), scale=(6,1,2), texture='brick', texture_scale=(8,8))
    hookshot_target = Button(parent=scene, model='cube', color=color.brown, position=(4,5,5))
    hookshot_target.on_click = Func(player.animate_position, hookshot_target.position, duration=.5, curve=curve.linear)

    def input(key):
        if key == "escape":
            application.quit()
        if key == 'left mouse down' and player.gun:
            gun.blink(color.orange)
            bullet = Entity(parent=gun, model='cube', scale=.1, color=color.black)
            bullet.world_parent = scene
            bullet.animate_position(bullet.position+(bullet.forward*50), curve=curve.linear, duration=1)
            destroy(bullet, delay=1)

    app.run()
