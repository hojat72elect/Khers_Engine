from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.video_recorder import VideoRecorder
from ursina.shaders import lit_with_shadows_shader
from ursina import Ursina, window, Entity, EditorCamera, BoxCollider, Vec3, camera, color, mouse, DirectionalLight, Sky, application
import random

if __name__ == '__main__':
    app = Ursina()
    window.size = (1280*.5, 720*.5)
    random.seed(0)
    Entity.default_shader = lit_with_shadows_shader
    ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))
    editor_camera = EditorCamera(enabled=False, ignore_paused=True)
    player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8)
    player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))
    gun = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.red, on_cooldown=False)
    shootables_parent = Entity()
    mouse.traverse_target = shootables_parent

    for i in range(16):
        Entity(
            model="cube",
            origin_y=-0.5,
            scale=2,
            texture="brick",
            texture_scale=(1, 2),
            x=random.uniform(-8, 8),
            z=random.uniform(-8, 8) + 8,
            collider="box",
            scale_y=random.uniform(2, 3),
            color=color.hsv(0, 0, random.uniform(0.9, 1)),
        )

    sun = DirectionalLight()
    sun.look_at(Vec3(1,-1,-1))
    Sky()
    vr = VideoRecorder(max_duration=120)

    def input(key):
        if key == "escape":
            application.quit()
    
    app.run()
