from ursina import *

app = Ursina()

# -----------------------------
# Game state
# -----------------------------
movement_speed = 5

# -----------------------------
# Background
# -----------------------------
background = Entity(
    model='quad',
    scale=(16, 16),
    color=color.white,
    z=1
)

# -----------------------------
# Potato
# -----------------------------
potato = Entity(
    model='quad',
    texture='../potato.png',
    scale=(
        0.5,  # adjust if your potato.png needs a different size
        0.5
    ),
    position=(-5, 0, 0)
)

# -----------------------------
# Target
# -----------------------------
target = Entity(
    model='quad',
    scale=(160 / 40, 280 / 40),
    position=(1.5, 1.5, -0.1),
    color=color.black
)

# -----------------------------
# Text
# -----------------------------
hello_text = Text(
    text='Hello World!',
    position=(0.0, 0.15),
    origin=(0, 0),
    color=color.black,
    scale=1.5
)

# -----------------------------
# Sound
# -----------------------------
clank_sound = Audio(
    '../clank.wav',
    autoplay=False
)

# Collision state
collision = False
mouse_collision = False


def update():
    global collision, mouse_collision

    # ---------------------------------
    # Movement using held_keys
    # ---------------------------------
    if held_keys['d']:
        potato.x += movement_speed * time.dt

    if held_keys['a']:
        potato.x -= movement_speed * time.dt

    if held_keys['w']:
        potato.y += movement_speed * time.dt

    if held_keys['s']:
        potato.y -= movement_speed * time.dt

    # ---------------------------------
    # Potato / target collision
    # ---------------------------------
    collision = potato.intersects(target).hit

    # ---------------------------------
    # Mouse / target collision
    # ---------------------------------
    mouse_world_position = mouse.world_point

    if mouse_world_position:
        mouse_collision = target.contains(mouse_world_position)
    else:
        mouse_collision = False

    # ---------------------------------
    # Target color
    # ---------------------------------
    if collision:
        target.color = color.red
    else:
        target.color = color.black


def input(key):
    # ---------------------------------
    # Quit
    # ---------------------------------
    if key == 'escape':
        application.quit()

    # ---------------------------------
    # Sound
    # ---------------------------------
    if key == 'f':
        clank_sound.play()


if __name__ == '__main__':
    app.run()
