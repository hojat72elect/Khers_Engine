from ursina import Ursina, Entity, color, Vec3, window, EditorCamera, curve, hsv, held_keys, scene, time, Path, Vec2
from ursina.prefabs.particle_system import ParticleSystem, ParticleSystemContainer, ParticleSystemUI
import random

if __name__ == '__main__':
    app = Ursina()

    player = Entity(model="wireframe_cube", color=color.magenta, origin_y=-0.5, alpha=1)
    run_particles = ParticleSystem(
        parent=player,
        scale=1,
        speed=1,
        spawn_interval=0.05,
        num_particles=1,
        mesh="icosphere",
        world_space=True,
        end_color=color.red,
        end_size=0,
        direction_randomness=Vec3(360),
        loop_every=0.1,
        auto_play=True,
    )
    EditorCamera()
    window.color = color.black

    S = 5
    spawn_points = [Vec3(*[random.uniform(-S,S) for _ in range(3)]) for i in range(1)]
    print(spawn_points)
    particle_system_container = ParticleSystemContainer(
        (
            ParticleSystem(
                start_size=(0.25, 0.25, 0.75),
                end_size=Vec3(8, 5, 1) * 0.5,
                size_curve=curve.combine(
                    curve.linear, curve.reverse(curve.in_expo), 0.33
                ),
                lifetime=0.4,
                auto_play=False,
                direction_randomness=Vec3(0, 0, 360),
                move_directions="up",
                mesh="cube",
                start_color=[
                    hsv(200 + (i * 10), 1 - (i * 0.1), 1) for i in range(12 * 2)
                ],
                end_color=[
                    hsv(200 + 20 + (i * 10), 0.5, 1 - (i * 0.15)) for i in range(12 * 2)
                ],
                color_curve=curve.linear,
                color_sample_function="sequential",
                num_particles=0,
                spawn_points=[Vec3(0, 0, z * 0.5) for z in range(12 * 2)],
                spawn_type="sequential",
                spawn_interval=0.0125 / 1,
                name="blink_particles",
                seed=2,
            ),
        )
    )
    particle_system_ui = ParticleSystemUI(Path(__file__), particle_system_container)

    def update():
        h = max((held_keys['gamepad left stick x'], held_keys['d']-held_keys['a']), key=lambda x: abs(x))
        v = max((held_keys['gamepad left stick y'], held_keys['w']-held_keys['s']), key=lambda x: abs(x))
        move_speed = 5
        input_direction = Vec3(h,0,v).normalized()
        input_strength = min(Vec3(h,0,v).length(), 1)
        player.look_at_xz(player.position + input_direction)
        player.position += player.forward * time.dt * move_speed * input_strength
        run_particles.ignore = input_strength < .01

    ground = Entity(model='plane', scale=8, texture='grass', texture_scale=Vec2(1), color=color.dark_gray)

    def input(key):
        if key == 'l':
            for e in scene.entities:
                if e.name:
                    print('e:', e.name)
                if e in scene._entities_marked_for_removal:
                    print('marked for removal:', e.name)

    app.run()
