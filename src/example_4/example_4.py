from ursina import *

app = Ursina(title="Endless Runner Game", borderless=False, size=(800, 600))
camera.orthographic = True
camera.fov = 20

# ── Constants (world-unit equivalents of the pyglet version) ──
GRAVITY = -30
JUMP_SPEED = 16
OBSTACLE_SPEED = 10
SPAWN_INTERVAL = 1.5

# ── Ground ──
ground = Entity(
    model='quad',
    color=color.blue,
    scale=(30, 0.7),
    position=(0, -4.5),
)

# ── Player ──
player = Entity(
    model='quad',
    color=color.rgb(50, 225, 30),
    scale=(1.5, 1.5),
    position=(-8, ground.y + ground.scale_y / 2 + 0.75),
)

player_velocity_y = 0
is_jumping = False
game_over = False

# ── Obstacles ──
obstacles = []


def create_obstacle():
    """Spawn a new red obstacle at the right edge of the screen."""
    if game_over:
        return
    height = random.uniform(0.7, 1.7)
    obstacle = Entity(
        model='quad',
        color=color.red,
        scale=(0.6, height),
        position=(
            camera.fov * (camera.aspect_ratio),
            ground.y + ground.scale_y / 2 + height / 2,
        ),
    )
    obstacles.append(obstacle)


spawn_timer = 0


def update():
    global player_velocity_y, is_jumping, game_over, spawn_timer

    if game_over:
        return

    dt = time.dt

    # ── Spawn obstacles on a timer ──
    spawn_timer += dt
    if spawn_timer >= SPAWN_INTERVAL:
        spawn_timer -= SPAWN_INTERVAL
        create_obstacle()

    # ── Player physics ──
    player_velocity_y += GRAVITY * dt
    player.y += player_velocity_y * dt

    ground_top = ground.y + ground.scale_y / 2 + player.scale_y / 2
    if player.y <= ground_top:
        player.y = ground_top
        player_velocity_y = 0
        is_jumping = False

    # ── Move & cull obstacles ──
    for obstacle in obstacles[:]:
        obstacle.x -= OBSTACLE_SPEED * dt
        if obstacle.x < -camera.fov * camera.aspect_ratio - 2:
            destroy(obstacle)
            obstacles.remove(obstacle)

    # ── Collision detection (AABB) ──
    px, py = player.x, player.y
    phw, phh = player.scale_x / 2, player.scale_y / 2

    for obstacle in obstacles:
        ox, oy = obstacle.x, obstacle.y
        ohw, ohh = obstacle.scale_x / 2, obstacle.scale_y / 2

        if (px + phw > ox - ohw and px - phw < ox + ohw and
                py - phh < oy + ohh and py + phh > oy - ohh):
            print("Game Over!")
            game_over = True
            game_over_text = Text(
                text='GAME OVER',
                origin=(0, 0),
                scale=3,
                color=color.white,
            )
            return


def input(key):
    global player_velocity_y, is_jumping

    if key == 'space' and not is_jumping and not game_over:
        player_velocity_y = JUMP_SPEED
        is_jumping = True

    if key == 'escape':
        application.quit()


app.run()
