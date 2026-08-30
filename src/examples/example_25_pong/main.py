from ursina import Ursina, window, color, camera, Entity, duplicate, Text, time, held_keys, curve, destroy, invoke

app = Ursina()

window.color = color.black
camera.orthographic = True
camera.fov = 1

left_paddle = Entity(scale=(1 / 32, 6 / 32), x=-0.75, model="quad", color=color.white, origin_x=0.5, collider="box")
right_paddle = duplicate(left_paddle, x=(-1) * left_paddle.x, rotation_z=left_paddle.rotation_z + 180)

floor = Entity(model="quad", y=-0.5, origin_y=0.5, collider="box", scale=(2, 10), visible=False)
ceiling = duplicate(floor, y=0.5, rotation_z=180, visible=False)
left_wall = duplicate(floor, x=-0.5 * window.aspect_ratio, rotation_z=90, visible=True)
right_wall = duplicate(floor, x=0.5 * window.aspect_ratio, rotation_z=-90, visible=True)

left_score = 0
right_score = 0
max_score = 5
is_game_paused = False
collision_cooldown = 0.15

ball = Entity(model="circle", scale=0.05, collider="box", speed=0, collision_cooldown=collision_cooldown)
score_text = Text(text=f"{left_score}:{right_score}", position=(0, 0.45), scale=2, origin=(0, 0))


def reset():
    ball.position = (0, 0, 0)
    ball.rotation = (0, 0, 0)
    ball.speed = 10
    for paddle in (left_paddle, right_paddle):
        paddle.collision = True
        paddle.y = 0


def update_score():
    global left_score, right_score, is_game_paused
    score_text.text = f"{left_score} : {right_score}"

    if left_score >= max_score or right_score >= max_score:
        winner_text = Text(f"{'Left' if left_score >= max_score else 'Right'} Player Wins!", y=0, scale=2, origin=(0, 0))
        ball.speed = 0
        game_paused = True  # Pause the game after a win
        invoke(destroy, winner_text, delay=3)
    else:
        reset()


def update():
    global left_score, right_score, is_game_paused, collision_cooldown
    if is_game_paused:
        return

    ball.collision_cooldown -= time.dt
    ball.position += ball.right * time.dt * ball.speed

    left_paddle.y += (held_keys["w"] - held_keys["s"]) * time.dt
    right_paddle.y += (held_keys["up arrow"] - held_keys["down arrow"]) * time.dt

    if ball.collision_cooldown > 0:
        return

    hit_info = ball.intersects()
    if hit_info.hit:
        ball.collision_cooldown = collision_cooldown

        if hit_info.entity in (left_paddle, right_paddle):
            ball.rotation_z += 180 * (-1 if hit_info.entity == left_paddle else 1)
            ball.rotation_z -= (hit_info.entity.world_y - ball.y) * 20 * 32 * (-1 if hit_info.entity == left_paddle else 1)
            ball.speed *= 1.1
        elif hit_info.entity == right_wall:
            left_score += 1
            update_score()
        elif hit_info.entity == left_wall:
            right_score += 1
            update_score()

        particle = Entity(model="quad", position=hit_info.world_point, scale=0, texture="circle", add_to_scene_entities=False)
        particle.animate_scale(0.2, 0.5, curve=curve.out_expo)
        particle.animate_color(color.clear, duration=0.5, curve=curve.out_expo)
        destroy(particle, delay=0.5)

    if ball.y > ceiling.y - ball.scale_y / 2 or ball.y < floor.y + ball.scale_y / 2:
        ball.rotation_z = -ball.rotation_z


info_text = Text("press space to play", y=-.45)


def input(key):
    global is_game_paused

    if key == "space" and not is_game_paused:
        info_text.enabled = False
        reset()


app.run()
