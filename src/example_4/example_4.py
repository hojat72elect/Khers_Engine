import random

import pyglet

window = pyglet.window.Window(width=800, height=600, caption="Endless Runner Game")

gravity = -900
jump_speed = 500
player_speed = 300

batch = pyglet.graphics.Batch()

player = pyglet.shapes.Rectangle(50, 100, 50, 50, color=(50, 225, 30), batch=batch)

ground = pyglet.shapes.Rectangle(0, 50, 800, 20, color=(0, 0, 255), batch=batch)

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
player_velocity_y = 0
is_jumping = False

obstacles = []


def create_obstacle():
    x = window.width
    y = ground.y + ground.height
    width = 20
    height = random.randint(20, 50)
    obstacle = pyglet.shapes.Rectangle(x, y, width, height, color=(255, 0, 0), batch=batch)
    obstacles.append(obstacle)


def update_obstacles(dt):
    for obstacle in obstacles:
        obstacle.x -= player_speed * dt
    obstacles[:] = [obstacle for obstacle in obstacles if obstacle.x + obstacle.width > 0]


def update(dt):
    global player_velocity_y, is_jumping

    player_velocity_y += gravity * dt
    player.y += player_velocity_y * dt

    if player.y <= ground.y + ground.height:
        player.y = ground.y + ground.height
        player_velocity_y = 0
        is_jumping = False

    for obstacle in obstacles:
        if (player.x + player.width > obstacle.x and player.x < obstacle.x + obstacle.width and
                player.y < obstacle.y + obstacle.height):
            print("Game Over!")
            pyglet.app.exit()

    update_obstacles(dt)


@window.event
def on_key_press(symbol, modifiers):
    global player_velocity_y, is_jumping

    # Handle jump
    if symbol == pyglet.window.key.SPACE and not is_jumping:
        player_velocity_y = jump_speed
        is_jumping = True


@window.event
def on_draw():
    window.clear()
    batch.draw()


pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.clock.schedule_interval(lambda dt: create_obstacle(), 1.5)

pyglet.app.run()
