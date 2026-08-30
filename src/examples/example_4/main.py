from random import uniform

from ursina import Ursina, camera, Entity, color, time, destroy, Text, application

from Player import Player

app = Ursina(title="Endless Runner Game", borderless=False, size=(800, 600))
camera.orthographic = True
camera.fov = 20
GRAVITY = -30
OBSTACLE_SPEED = 10
SPAWN_INTERVAL = 1.5

ground = Entity(model='quad', color=color.blue, scale=(30, 0.7), position=(0, -4.5))
player = Player(ground)

game_over = False
obstacles = []
spawn_timer = 0


def update():
    global game_over, spawn_timer
    global player
    if game_over:
        return
    dt = time.dt
    spawn_timer += dt
    if spawn_timer >= SPAWN_INTERVAL:
        spawn_timer -= SPAWN_INTERVAL
        if game_over:
            return
        height = uniform(0.7, 1.7)
        obstacle = Entity(model='quad', color=color.red, scale=(0.6, height), position=(camera.fov * camera.aspect_ratio, ground.y + ground.scale_y / 2 + height / 2))
        obstacles.append(obstacle)
    player.vertical_velocity += GRAVITY * dt
    player.entity.y += player.vertical_velocity * dt
    ground_top = ground.y + ground.scale_y / 2 + player.entity.scale_y / 2
    if player.entity.y <= ground_top:
        player.entity.y = ground_top
        player.vertical_velocity = 0
        player.is_jumping = False

    for obstacle in obstacles[:]:
        obstacle.x -= OBSTACLE_SPEED * dt
        if obstacle.x < -camera.fov * camera.aspect_ratio - 2:
            destroy(obstacle)
            obstacles.remove(obstacle)

    px, py = player.entity.x, player.entity.y
    phw, phh = player.entity.scale_x / 2, player.entity.scale_y / 2
    for obstacle in obstacles:
        ox, oy = obstacle.x, obstacle.y
        ohw, ohh = obstacle.scale_x / 2, obstacle.scale_y / 2
        if (px + phw > ox - ohw and px - phw < ox + ohw and
                py - phh < oy + ohh and py + phh > oy - ohh):
            game_over = True
            Text(text='GAME OVER', origin=(0, 0), scale=3, color=color.white)
            return


def input(key):
    global player
    if key == 'space' and not player.is_jumping and not game_over:
        player.vertical_velocity = Player.JUMP_SPEED
        player.is_jumping = True
    if key == 'escape':
        application.quit()


app.run()
