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
    position=(-5, 0, 0),
    collider='box'
)

# -----------------------------
# Target
# -----------------------------
target = Entity(
    model='quad',
    scale=(160 / 40, 280 / 40),
    position=(1.5, 1.5, 0),
    color=color.black,
    collider='box'
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
    hit_info = potato.intersects(target)
    collision = hit_info.hit
    print(f"Collision: {collision}, Potato: ({potato.x:.2f}, {potato.y:.2f}), Target: ({target.x:.2f}, {target.y:.2f}), HitInfo: {hit_info}")

    # ---------------------------------
    # Mouse / target collision
    # ---------------------------------
    mouse_collision = mouse.hovered_entity == target

    # ---------------------------------
    # Target color
    # ---------------------------------
    if collision:
        target.color = color.red
    elif mouse_collision:
        target.color = color.blue
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
