from ursina import *

# ============================================================
# Configuration
# ============================================================

GAME_WIDTH = 800
GAME_HEIGHT = 600

# ============================================================
# Ursina application
# ============================================================

app = Ursina(
    title="Breakout",
    size=(GAME_WIDTH, GAME_HEIGHT),
    forced_aspect_ratio=GAME_WIDTH / GAME_HEIGHT,
)

# We want a 2D game with an 800x600 coordinate system.
camera.orthographic = True
camera.fov = GAME_HEIGHT

# Same background as the Phaser game.
window.color = color.rgb(2, 138, 248)

# Keep pixel-art textures sharp.
Texture.default_filtering = None


# ============================================================
# Phaser -> Ursina coordinate conversion
#
# Phaser:
#
#       (0, 0) ----------------> (800, 0)
#         |
#         |
#         |
#         v
#       (0, 600)
#
#
# Ursina:
#
#                 y+
#                 |
#                 |
#       x- -------+------- x+
#                 |
#                 |
#                 y-
#
# We therefore translate Phaser coordinates into centered
# Ursina coordinates.
# ============================================================

def px(x):
    return x - GAME_WIDTH / 2


def py(y):
    return GAME_HEIGHT / 2 - y


def to_phaser_x(x):
    return x + GAME_WIDTH / 2


def to_phaser_y(y):
    return GAME_HEIGHT / 2 - y


# ============================================================
# Create a sprite using one of the existing PNG files
# ============================================================

def create_sprite(
        image_name,
        x,
        y,
        z=0
):
    entity = Entity(
        model="quad",
        texture=f"{image_name}.png",
        position=(px(x), py(y), z),
    )

    return entity


# ============================================================
# Game objects
# ============================================================

ball = None
paddle = None
bricks = []

# ============================================================
# Game state
# ============================================================

ball_on_paddle = True

ball_velocity_x = 0.0
ball_velocity_y = 0.0

# ============================================================
# Game constants
# ============================================================

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


# ============================================================
# Create bricks
# ============================================================

def create_bricks():
    global bricks

    bricks = []

    for row in range(BRICK_ROWS):

        for column in range(BRICK_COLUMNS):
            x = (
                    BRICK_START_X
                    + column * BRICK_CELL_WIDTH
            )

            y = (
                    BRICK_START_Y
                    + row * BRICK_CELL_HEIGHT
            )

            brick = create_sprite(
                BRICK_TYPES[row],
                x,
                y,
                z=1,
            )

            bricks.append(brick)


# ============================================================
# Create ball
# ============================================================

def create_ball():
    global ball

    ball = create_sprite(
        "ball1",
        BALL_START_X,
        BALL_START_Y,
        z=2,
    )


# ============================================================
# Create paddle
# ============================================================

def create_paddle():
    global paddle

    paddle = create_sprite(
        "paddle1",
        PADDLE_START_X,
        PADDLE_Y,
        z=2,
    )


# ============================================================
# Get dimensions
# ============================================================

def width(entity):
    return entity.scale_x


def height(entity):
    return entity.scale_y


# ============================================================
# AABB collision
# ============================================================

def intersects(a, b):
    return (
            abs(a.x - b.x)
            < (width(a) + width(b)) / 2
            and
            abs(a.y - b.y)
            < (height(a) + height(b)) / 2
    )


# ============================================================
# Reset ball
# ============================================================

def reset_ball():
    global ball_on_paddle
    global ball_velocity_x
    global ball_velocity_y

    ball_velocity_x = 0
    ball_velocity_y = 0

    ball.x = paddle.x
    ball.y = py(BALL_START_Y)

    ball_on_paddle = True


# ============================================================
# Reset level
# ============================================================

def reset_level():
    for brick in bricks:
        brick.enabled = True

    reset_ball()


# ============================================================
# Launch ball
# ============================================================

def launch_ball():
    global ball_on_paddle
    global ball_velocity_x
    global ball_velocity_y

    if not ball_on_paddle:
        return

    # Exactly like the original Phaser code:
    #
    # this.ball.setVelocity(-75, -300);

    ball_velocity_x = -75
    ball_velocity_y = -300

    ball_on_paddle = False


# ============================================================
# Paddle movement
# ============================================================

def update_paddle():
    # Ursina mouse.x:
    #
    #       -0.5 ... +0.5
    #
    # Convert to:
    #
    #       0 ... 800
    #

    mouse_x = (mouse.x + 0.5) * GAME_WIDTH

    mouse_x = clamp(
        mouse_x,
        PADDLE_MIN_X,
        PADDLE_MAX_X,
    )

    paddle.x = px(mouse_x)

    # Phaser:
    #
    # if (this.ball.getData('onPaddle')) {
    #     this.ball.x = this.paddle.x;
    # }

    if ball_on_paddle:
        ball.x = paddle.x


# ============================================================
# Paddle collision
# ============================================================

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

        ball_velocity_x = (
                2 + random.random() * 8
        )


# ============================================================
# Check paddle collision
# ============================================================

def check_paddle_collision():
    global ball_velocity_y

    if not intersects(ball, paddle):
        return

    # Don't collide while the ball is travelling upward.
    if ball_velocity_y <= 0:
        return

    # Put the ball just above the paddle.
    ball.y = (
            paddle.y
            + (height(ball) + height(paddle)) / 2
    )

    # Bounce upward.
    ball_velocity_y = -abs(ball_velocity_y)

    hit_paddle()


# ============================================================
# Brick collision
# ============================================================

def check_brick_collisions():
    global ball_velocity_x
    global ball_velocity_y

    for brick in bricks:

        if not brick.enabled:
            continue

        if not intersects(ball, brick):
            continue

        # Distance between centers.
        dx = ball.x - brick.x
        dy = ball.y - brick.y

        # Calculate overlap.
        overlap_x = (
                            width(ball) + width(brick)
                    ) / 2 - abs(dx)

        overlap_y = (
                            height(ball) + height(brick)
                    ) / 2 - abs(dy)

        # ----------------------------------------
        # Horizontal collision
        # ----------------------------------------

        if overlap_x < overlap_y:

            ball_velocity_x *= -1

            if dx > 0:
                ball.x = (
                        brick.x
                        + (width(ball) + width(brick)) / 2
                )
            else:
                ball.x = (
                        brick.x
                        - (width(ball) + width(brick)) / 2
                )

        # ----------------------------------------
        # Vertical collision
        # ----------------------------------------

        else:

            ball_velocity_y *= -1

            if dy > 0:
                ball.y = (
                        brick.y
                        + (height(ball) + height(brick)) / 2
                )
            else:
                ball.y = (
                        brick.y
                        - (height(ball) + height(brick)) / 2
                )

        # Phaser:
        #
        # brick.disableBody(true, true);
        #
        brick.enabled = False

        # Phaser:
        #
        # if (this.bricks.countActive() === 0) {
        #     this.resetLevel();
        # }

        if not any(
                brick.enabled
                for brick in bricks
        ):
            reset_level()

        # Don't process another brick this frame.
        break


# ============================================================
# World bounds
# ============================================================

def check_world_bounds():
    global ball_velocity_x
    global ball_velocity_y

    x = to_phaser_x(ball.x)
    y = to_phaser_y(ball.y)

    half_width = width(ball) / 2
    half_height = height(ball) / 2

    # ----------------------------------------
    # Left wall
    # ----------------------------------------

    if x - half_width <= 0:
        x = half_width

        ball_velocity_x = abs(
            ball_velocity_x
        )

        ball.x = px(x)

    # ----------------------------------------
    # Right wall
    # ----------------------------------------

    if x + half_width >= GAME_WIDTH:
        x = GAME_WIDTH - half_width

        ball_velocity_x = -abs(
            ball_velocity_x
        )

        ball.x = px(x)

    # ----------------------------------------
    # Top wall
    # ----------------------------------------

    if y - half_height <= 0:
        y = half_height

        ball_velocity_y = abs(
            ball_velocity_y
        )

        ball.y = py(y)

    # ----------------------------------------
    # Bottom
    # ----------------------------------------
    #
    # Phaser has:
    #
    # setBoundsCollision(true, true, true, false)
    #
    # so the bottom collision is disabled.
    #
    # The original game therefore resets the ball
    # when it falls below the screen.
    #

    if y > GAME_HEIGHT:
        reset_ball()


# ============================================================
# Game update
# ============================================================

def update():
    global ball_velocity_x
    global ball_velocity_y

    # Move paddle according to mouse.
    update_paddle()

    # Ball is waiting on the paddle.
    if ball_on_paddle:
        ball.x = paddle.x
        return

    # --------------------------------------------------------
    # Move ball.
    #
    # Phaser's velocity:
    #
    #     +Y = down
    #
    # Ursina:
    #
    #     +Y = up
    #
    # Therefore we subtract the Phaser Y velocity.
    # --------------------------------------------------------

    ball.x += ball_velocity_x * time.dt
    ball.y -= ball_velocity_y * time.dt

    # Check walls.
    check_world_bounds()

    # The ball may have been reset.
    if ball_on_paddle:
        return

    # Paddle.
    check_paddle_collision()

    # Bricks.
    check_brick_collisions()


# ============================================================
# Input
# ============================================================

def input(key):
    # Phaser's pointerup.
    if key == "left mouse up":
        launch_ball()

    # Convenient keyboard alternative.
    if key == "space":
        launch_ball()


# ============================================================
# Initialize
# ============================================================

create_bricks()
create_ball()
create_paddle()

reset_ball()

# ============================================================
# Run
# ============================================================

app.run()
