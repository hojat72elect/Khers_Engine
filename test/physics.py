from ursina import Ursina, Vec2, Capsule, lerp_exponential_decay, Sequence, time, held_keys, raycast, EditorCamera, Entity, Vec3, color, camera, scene, destroy
from ursina.physics import PhysicsEntity, physics_handler, CapsuleCollider

if __name__ == '__main__':
    app = Ursina(borderless=False)

    class Player(PhysicsEntity):
        def __init__(self, **kwargs):
            super().__init__(collider=CapsuleCollider(), model=Capsule(), color=color.orange, y=2, z=0, mass=1, friction=1, lock_axis=Vec3(0, 0, 0), lock_rotation=Vec3(1, 1, 1), rotational_friction=Vec3.zero)
            Entity(parent=self, model='sphere', z=.2, y=.25, scale=1, color=color.red)

            self.camera_controller = EditorCamera(pan_speed=Vec2.zero)

            self.rotation_helper = Entity(loose_parent=self, model='wireframe_cube', visible=False)
            def rotation_helper_update():
                self.rotation_helper.position = self.position
                self.rotation_helper.rotation_y = self.camera_controller.rotation_y
            self.rotation_helper.update = rotation_helper_update

            self.direction_helper = Entity(parent=self.rotation_helper, scale=.2, model='sphere', always_on_top=True, enabled=1, color=color.pink, visible=False)
            self.helper = Entity(parent=self)
            for key, value in kwargs.items():
                setattr(self, key, value)
            self.physics_update_loop = Sequence(self.physics_update, 1/30, loop=True, started=True)

        def update(self):
            self.camera_controller.position = lerp_exponential_decay(self.camera_controller.position, self.position, time.dt*10)

        def physics_update(self):
            h = max((held_keys['gamepad left stick x'], held_keys['d']-held_keys['a']), key=lambda x: abs(x))
            v = max((held_keys['gamepad left stick y'], held_keys['w']-held_keys['s']), key=lambda x: abs(x))
            direction = Vec3(h, 0, v).normalized()
            limit = 14
            self.friction = 10 if direction.length() < 0.1 else .5

            self.input_strength = min(Vec3(h, 0, v).length(), 1)
            if self.input_strength:
                self.direction_helper.position = direction * 3
                self.helper.look_at_2d(self.direction_helper.world_position, 'y')

                vel = self.velocity
                xz_vel = (self.helper.forward * 100 * self.input_strength).xz
                speed = xz_vel.length()
                if speed > limit:
                    xz_vel.normalize()
                    xz_vel *= limit
                vel.x = xz_vel.x
                vel.z = xz_vel.y
                self.velocity = vel

            self.grounded = raycast(self.position+(Vec3.down*.9), Vec3.down, distance=.2).hit
            self.color = color.orange if self.grounded else color.azure
            if not self.grounded:   # prevent sticking to walls
                self.friction = 0

        def input(self, key):
            if key in 'wasd ':
                self.physics_update()
            if key == 'space':
                print('jump')
                self.velocity = Vec3.zero
                self.apply_impulse(Vec3.up * 18)

    player = Player(x=10, z=-10)
    ground = PhysicsEntity(model='cube', origin_y=.5, texture='grass', scale=Vec3(30, 1, 30), collider='box')
    cube = PhysicsEntity(model='cube', texture='white_cube', x=2, y=3, collider='box', color=color.lime, mass=0)
    cube_with_origin = PhysicsEntity(model='icosphere', origin=(0, -0.5, 0), scale=2, x=-1, y=3, z=-3, collider='sphere', color=color.orange, mass=0)
    slope = PhysicsEntity(model='plane', collider='box', scale=10, x=-8, z=10, rotation_x=-30, y=2, color=color.red)
    icosphere = PhysicsEntity(model='icosphere', collider='mesh', scale=4, x=10, z=0, y=2, color=color.violet)
    icosphere_2 = PhysicsEntity(model='icosphere', collider='mesh', scale=.5, color=color.green)
    e = PhysicsEntity(z=-2)
    sphere = PhysicsEntity(parent=e, model='icosphere', collider='sphere', x=-4, scale=3, color=color.blue, )
    ground = PhysicsEntity(model='cube', scale=10, collider='box', x=-8, z=-10, rotation_x=-10, y=-5, color=color.gray, name='ground')
    camera.fov = 100
    mover = PhysicsEntity(model='cube', color=color.red)
    child = PhysicsEntity(parent=mover, model='cube', origin_y=-.5, scale=2, collider='box', color=color.pink, x=-1)

    def input(key):
        if key == 't':
            sphere.enabled = not sphere.enabled
        if key == 'w':
            mover.z += 1
        if key == 'c':
            for e in scene.entities:
                if e == player or e.parent==player:
                    continue
                if isinstance(e, PhysicsEntity):
                    destroy(e)

    physics_handler.gravity = 50
    physics_handler.show_debug = True
    print('----------------------------', physics_handler.show_debug)

    app.run()
