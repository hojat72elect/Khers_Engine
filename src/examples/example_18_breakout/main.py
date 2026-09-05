from ursina import Ursina, camera, window, color, Entity, Texture, mouse, time, random, clamp

GAME_WIDTH = 800
GAME_HEIGHT = 600
app = Ursina(title="Breakout", size=(GAME_WIDTH, GAME_HEIGHT), forced_aspect_ratio=GAME_WIDTH / GAME_HEIGHT, )
camera.orthographic = True
camera.fov = GAME_HEIGHT
window.color = color.rgb(2, 138, 248)
Texture.default_filtering = None

def px(x):
    return x - GAME_WIDTH / 2

def py(y):
    return GAME_HEIGHT / 2 - y

def to_phaser_x(x):
    return x + GAME_WIDTH / 2

def to_phaser_y(y):
    return GAME_HEIGHT / 2 - y

def create_sprite(image_name, x, y, z=0):
    entity = Entity(model="quad", texture=f"assets/{image_name}.png", position=(px(x), py(y), z))

    if entity.texture:
        entity.scale_x = entity.texture.width
        entity.scale_y = entity.texture.height
    return entity

ball = None
paddle = None
bricks = []
ball_on_paddle = True
ball_velocity_x = 0.0
ball_velocity_y = 0.0
BALL_START_X = 400
BALL_START_Y = 500
PADDLE_START_X = 400
PADDLE_Y = 550
PADDLE_MIN_X = 52
PADDLE_MAX_X = 748
BRICK_START_X = 112
BRICK_START_Y = 100
BRICK_COLUMNS = 10
BRICK_ROWS = 6
BRICK_CELL_WIDTH = 64
BRICK_CELL_HEIGHT = 32

BRICK_TYPES = [
    "blue1",
    "red1",
    "green1",
    "yellow1",
    "silver1",
    "purple1",
]

def create_bricks():
    global bricks
    bricks = []
    for row in range(BRICK_ROWS):
        for column in range(BRICK_COLUMNS):
            x = (BRICK_START_X + column * BRICK_CELL_WIDTH)
            y = (BRICK_START_Y + row * BRICK_CELL_HEIGHT)
            brick = create_sprite(BRICK_TYPES[row], x, y, z=1)
            bricks.append(brick)

def create_ball():
    global ball
    ball = create_sprite("ball1", BALL_START_X, BALL_START_Y, z=2)

def create_paddle():
    global paddle
    paddle = create_sprite(
        "paddle1",
        PADDLE_START_X,
        PADDLE_Y,
        z=2,
    )

def width(entity):
    return entity.scale_x

def height(entity):
    return entity.scale_y

def intersects(a, b):
    return abs(a.x - b.x) < (width(a) + width(b)) / 2 and abs(a.y - b.y) < (height(a) + height(b)) / 2

def reset_ball():
    global ball_on_paddle
    global ball_velocity_x
    global ball_velocity_y
    ball_velocity_x = 0
    ball_velocity_y = 0
    ball.x = paddle.x
    ball.y = py(BALL_START_Y)
    ball_on_paddle = True

def reset_level():
    for brick in bricks:
        brick.enabled = True
    reset_ball()

def launch_ball():
    global ball_on_paddle
    global ball_velocity_x
    global ball_velocity_y
    if not ball_on_paddle:
        return
    ball_velocity_x = -75
    ball_velocity_y = -300
    ball_on_paddle = False

def update_paddle():
    mouse_x = (mouse.x + 0.5) * GAME_WIDTH
    mouse_x = clamp(mouse_x, PADDLE_MIN_X, PADDLE_MAX_X, )
    paddle.x = px(mouse_x)
    if ball_on_paddle:
        ball.x = paddle.x

def hit_paddle():
    global ball_velocity_x
    ball_x = to_phaser_x(ball.x)
    paddle_x = to_phaser_x(paddle.x)
    diff = 0

    if ball_x < paddle_x:
        diff = paddle_x - ball_x
        ball_velocity_x = -10 * diff
    elif ball_x > paddle_x:
        diff = ball_x - paddle_x
        ball_velocity_x = 10 * diff
    else:
        ball_velocity_x = (2 + random.random() * 8)

def check_paddle_collision():
    global ball_velocity_y
    if not intersects(ball, paddle):
        return
    if ball_velocity_y <= 0:
        return

    ball.y = (paddle.y + (height(ball) + height(paddle)) / 2)
    ball_velocity_y = -abs(ball_velocity_y)
    hit_paddle()

def check_brick_collisions():
    global ball_velocity_x
    global ball_velocity_y
    for brick in bricks:
        if not brick.enabled:
            continue
        if not intersects(ball, brick):
            continue

        dx = ball.x - brick.x
        dy = ball.y - brick.y
        overlap_x = (width(ball) + width(brick)) / 2 - abs(dx)
        overlap_y = (height(ball) + height(brick)) / 2 - abs(dy)

        if overlap_x < overlap_y:
            ball_velocity_x *= -1
            if dx > 0:
                ball.x = (brick.x + (width(ball) + width(brick)) / 2)
            else:
                ball.x = (brick.x - (width(ball) + width(brick)) / 2)
        else:
            ball_velocity_y *= -1
            if dy > 0:
                ball.y = (brick.y + (height(ball) + height(brick)) / 2)
            else:
                ball.y = (brick.y - (height(ball) + height(brick)) / 2)
        brick.enabled = False

        if not any(
                brick.enabled
                for brick in bricks
        ):
            reset_level()
        break

def check_world_bounds():
    global ball_velocity_x
    global ball_velocity_y
    x = to_phaser_x(ball.x)
    y = to_phaser_y(ball.y)
    half_width = width(ball) / 2
    half_height = height(ball) / 2

    if x - half_width <= 0:
        x = half_width
        ball_velocity_x = abs(ball_velocity_x)
        ball.x = px(x)
    if x + half_width >= GAME_WIDTH:
        x = GAME_WIDTH - half_width
        ball_velocity_x = -abs(ball_velocity_x)
        ball.x = px(x)
    if y - half_height <= 0:
        y = half_height
        ball_velocity_y = abs(ball_velocity_y)
        ball.y = py(y)
    if y > GAME_HEIGHT:
        reset_ball()

def update():
    global ball_velocity_x
    global ball_velocity_y
    update_paddle()
    if ball_on_paddle:
        ball.x = paddle.x
        return

    ball.x += ball_velocity_x * time.dt
    ball.y -= ball_velocity_y * time.dt
    check_world_bounds()
    if ball_on_paddle:
        return
    check_paddle_collision()
    check_brick_collisions()

def input(key):
    if key == "left mouse up":
        launch_ball()
    if key == "space":
        launch_ball()

create_bricks()
create_ball()
create_paddle()
reset_ball()
app.run()
