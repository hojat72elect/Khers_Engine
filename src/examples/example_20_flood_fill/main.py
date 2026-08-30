import random as py_random

from ursina import Ursina, Entity, Text, camera, window, color, Texture, mouse, time, destroy, invoke, Vec3, curve

GAME_WIDTH = 800
GAME_HEIGHT = 600
app = Ursina(title="Flood Fill", size=(960, 720), forced_aspect_ratio=GAME_WIDTH / GAME_HEIGHT)
camera.orthographic = True
camera.fov = GAME_HEIGHT
Texture.default_filtering = None
window.color = color.black


def px(x):
    return x - GAME_WIDTH / 2


def py(y):
    return GAME_HEIGHT / 2 - y


def to_game_x(x):
    return x + GAME_WIDTH / 2


def to_game_y(y):
    return GAME_HEIGHT / 2 - y


def create_sprite(image_name, x, y, z=0, scale=None):
    entity = Entity(model="quad", texture=f"assets/{image_name}.png", position=(px(x), py(y), z))
    if entity.texture:
        if scale is None:
            entity.scale_x = entity.texture.width
            entity.scale_y = entity.texture.height
        else:
            entity.scale = scale
    return entity


GRID_SIZE = 14
CELL_SIZE = 36
GRID_X = 166
GRID_Y = 66
COLORS = ["blue", "green", "grey", "purple", "red", "yellow"]
ICON_POSITIONS = [("grey", 16, 156), ("red", 16, 312), ("green", 16, 458), ("yellow", 688, 156), ("blue", 688, 312), ("purple", 688, 458)]
grid = []
current_color = 0
moves = 25
allow_click = False
game_over = False
matched = []
particles = []
background = None
grid_background = None
cursor_indicator = None
arrow = None
text_moves = None
text_number = None
text_message = None
instructions = None
icons = {}
monster_bounce = None
monster_bounce_time = 0
arrow_base_x = 109 - 24
arrow_time = 0


def random_color():
    return py_random.randrange(len(COLORS))


def color_frame(index):
    return COLORS[index]


def create_text(text, x, y, size=24, alpha=1):
    return Text(text=text, position=(px(x) / GAME_WIDTH, py(y) / GAME_HEIGHT,), origin=(0, 0), scale=size / 24, color=color.white, alpha=alpha)


def create_grid():
    global grid
    grid = []

    for x in range(GRID_SIZE):
        column = []

        for y in range(GRID_SIZE):
            game_x = GRID_X + x * CELL_SIZE
            game_y = GRID_Y + y * CELL_SIZE
            color_index = random_color()
            block = create_sprite(COLORS[color_index], game_x, game_y, z=100)
            block.grid_x = x
            block.grid_y = y
            block.current_color = color_index
            block.target_x = game_x
            block.target_y = game_y
            column.append(block)

        grid.append(column)


def get_block(x, y):
    if x < 0 or x >= GRID_SIZE:
        return None
    if y < 0 or y >= GRID_SIZE:
        return None
    return grid[x][y]


def flood_fill(old_color, new_color, start_x, start_y):
    global matched
    matched = []

    if old_color == new_color:
        return
    if get_block(start_x, start_y) is None:
        return
    if get_block(start_x, start_y).current_color != old_color:
        return

    stack = [(start_x, start_y)]
    visited = set()
    while stack:
        x, y = stack.pop()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        block = get_block(x, y)
        if block is None:
            continue
        if block.current_color != old_color:
            continue

        block.old_color = old_color
        block.current_color = new_color
        matched.append(block)
        stack.append((x - 1, y))
        stack.append((x + 1, y))
        stack.append((x, y - 1))
        stack.append((x, y + 1))


def help_flood():
    for _ in range(8):
        x = py_random.randrange(14)
        y = py_random.randrange(14)
        block = get_block(x, y)
        old_color = block.current_color
        new_color = (old_color + 1) % len(COLORS)
        flood_fill(old_color, new_color, x, y)

    for block in matched:
        block.texture = f"{COLORS[block.current_color]}.png"


def create_icons():
    global icons
    for color_name, x, y in ICON_POSITIONS:

        monster = create_sprite(f"icon-{color_name}", x, y, z=5)
        shadow = create_sprite("shadow", x, y, z=4)
        shadow.color = color.white
        shadow.collider = "box"
        shadow.icon_color = COLORS.index(color_name)
        shadow.monster = monster
        shadow.icon_x = x
        shadow.icon_y = y

        if x < 400:
            monster.x = px(-200)
            shadow.x = px(-200)
        else:
            monster.x = px(1000)
            shadow.x = px(1000)

        icons[color_name] = {"monster": monster, "shadow": shadow, "x": x, "y": y}


def create_cursor():
    global cursor_indicator
    cursor_indicator = create_sprite("cursor-over", 0, 0, z=10)
    cursor_indicator.enabled = False


def create_arrow():
    global arrow
    arrow = create_sprite("arrow-white", arrow_base_x, 48, z=10)
    arrow.alpha = 0


class Particle(Entity):

    def __init__(self, x, y, texture_name):
        super().__init__(model="quad", texture=f"assets/{texture_name}.png", position=(px(x), py(y), 20))
        self.scale_x = self.texture.width * 0.5
        self.scale_y = self.texture.height * 0.5
        self.velocity = Vec3(py_random.uniform(-160, 160), py_random.uniform(-180, 80), 0)
        self.life = 1.0
        self.rotation_speed = py_random.uniform(-360, 360)
        particles.append(self)

    def update_particle(self):
        self.x += self.velocity.x * time.dt
        self.y += self.velocity.y * time.dt
        self.velocity.y -= 350 * time.dt
        self.rotation_z += self.rotation_speed * time.dt
        self.life -= time.dt
        self.alpha = max(0, self.life)
        self.scale_x *= 0.985
        self.scale_y *= 0.985
        if self.life <= 0:
            if self in particles:
                particles.remove(self)
            destroy(self)


def explode_particles(texture_name, x, y, amount=6):
    for _ in range(amount):
        Particle(x, y, texture_name)


def animate_block_change(block, new_color, delay):
    def change():
        block.texture = f"{COLORS[new_color]}.png"
        explode_particles(
            COLORS[block.old_color],
            to_game_x(block.x),
            to_game_y(block.y),
            6,
        )

    invoke(change, delay=delay)


def reveal_grid():
    global allow_click
    grid_background.animate_y(py(300), duration=0.8, curve=curve.in_out_quad)
    delay = 0.8

    for y in range(13, -1, -1):
        for x in range(14):
            block = grid[x][y]
            block.animate_y(py(block.target_y), duration=0.8, delay=delay, curve=curve.in_out_quad)
            delay += 0.02

    icon_delay = delay - 1.0

    for data in [
        icons["grey"],
        icons["yellow"],
    ]:
        data["monster"].animate_x(px(data["x"]), duration=0.8, delay=icon_delay, curve=curve.in_out_quad)
        data["shadow"].animate_x(px(data["x"]), duration=0.8, delay=icon_delay, curve=curve.in_out_quad)

    icon_delay += 0.2
    for data in [
        icons["red"],
        icons["blue"],
    ]:
        data["monster"].animate_x(px(data["x"]), duration=0.8, delay=icon_delay, curve=curve.in_out_quad)
        data["shadow"].animate_x(px(data["x"]), duration=0.8, delay=icon_delay, curve=curve.in_out_quad)

    icon_delay += 0.2

    for data in [
        icons["green"],
        icons["purple"],
    ]:
        data["monster"].animate_x(px(data["x"]), duration=0.8, delay=icon_delay, curve=curve.in_out_quad)
        data["shadow"].animate_x(px(data["x"]), duration=0.8, delay=icon_delay, curve=curve.in_out_quad)

    text_moves.animate('alpha', 1, duration=0.5, delay=icon_delay)
    text_number.animate('alpha', 1, duration=0.5, delay=icon_delay)
    instructions.animate('alpha', 1, duration=0.5, delay=icon_delay + 1.0)
    arrow.animate('alpha', 1, duration=0.5, delay=icon_delay + 1.0)
    invoke(enable_input, delay=icon_delay + 1.5)


def enable_input():
    global allow_click
    allow_click = True


def icon_hovered(data):
    global monster_bounce
    global monster_bounce_time

    icon_color = COLORS.index(next(name for name, value in icons.items() if value is data))
    if icon_color == current_color:
        cursor_indicator.texture = "cursor-invalid.png"
    else:
        cursor_indicator.texture = "cursor-over.png"

    cursor_indicator.x = px(data["x"] + 48)
    cursor_indicator.y = py(data["y"] + 48)
    cursor_indicator.enabled = True
    cursor_indicator.alpha = 1
    arrow.texture = f"arrow-{COLORS[icon_color]}.png"
    monster = data["monster"]
    monster_bounce = monster
    monster_bounce_time = 0


def icon_clicked(data):
    global current_color
    global moves
    global matched
    global allow_click

    if not allow_click:
        return

    new_color = data["shadow"].icon_color
    if new_color == current_color:
        return
    old_color = grid[0][0].current_color
    current_color = new_color
    matched = []
    cursor_indicator.enabled = False
    instructions.enabled = False
    moves -= 1
    text_number.text = str(moves).zfill(2)
    flood_fill(old_color, new_color, 0, 0)

    if matched:
        start_flow()


def start_flow():
    global allow_click
    matched.sort(
        key=lambda block: (
                (to_game_x(block.x) - 166) ** 2
                + (to_game_y(block.y) - 66) ** 2
        )
    )

    allow_click = False

    if len(matched) > 98:
        increment = 0.006
    else:
        increment = 0.012

    for index, block in enumerate(matched):
        delay = index * increment
        old_color = block.old_color
        new_color = block.current_color
        animate_block_change(
            block,
            new_color,
            delay,
        )

    total_time = len(matched) * increment + 0.05
    invoke(finish_flow, delay=total_time)


def finish_flow():
    global allow_click
    allow_click = True
    if check_won():
        game_won()
    elif moves <= 0:
        game_lost()


def check_won():
    top_left = grid[0][0].current_color

    for x in range(14):
        for y in range(14):
            if grid[x][y].current_color != top_left:
                return False
    return True


def clear_grid():
    global allow_click

    allow_click = False

    for data in icons.values():
        data["monster"].animate('alpha', 0, duration=0.5, delay=0.5)
        data["shadow"].animate('alpha', 0, duration=0.5, delay=0.5)

    arrow.animate('alpha', 0, duration=0.5, delay=0.5)
    cursor_indicator.enabled = False
    delay = 0.5

    for y in range(13, -1, -1):
        for x in range(14):
            block = grid[x][y]
            block.animate_scale(0, duration=0.8, delay=delay, curve=curve.in_out_quad)
            delay += 0.01

    return delay + 0.8


def game_lost():
    global game_over
    game_over = True
    text_moves.text = "Lost!"
    text_number.text = ":("
    duration = clear_grid()
    text_message.text = "So close!\n\nClick to\ntry again"
    text_message.enabled = True
    text_message.alpha = 0
    text_message.animate('alpha', 1, duration=1, delay=duration)


def game_won():
    global game_over
    game_over = True
    text_moves.text = "Won!!"
    text_number.text = ":)"
    duration = clear_grid()
    monster_name = COLORS[current_color]
    winner = create_sprite(f"icon-{monster_name}", 400, 300, z=30)
    winner.scale = 0
    winner.animate_scale(4, duration=1, delay=duration, curve=curve.out_back)
    winner.animate_rotation_z(1440, duration=1, delay=duration)
    invoke(start_win_particles, delay=duration + 1.5)


def start_win_particles():
    explode_random_particles()
    invoke(explode_random_particles, delay=0.12)
    invoke(explode_random_particles, delay=0.24)
    invoke(explode_random_particles, delay=0.36)
    invoke(explode_random_particles, delay=0.48)


def explode_random_particles():
    texture_name = py_random.choice(COLORS)
    x = py_random.randint(128, 672)
    y = py_random.randint(28, 572)
    explode_particles(texture_name, x, y, 8)


def reset_game():
    global moves
    global game_over
    global allow_click
    global current_color
    global matched
    game_over = False
    allow_click = False
    moves = 25
    text_moves.text = "Moves"
    text_number.text = "00"
    text_message.enabled = False
    arrow.texture = "arrow-white.png"
    for data in icons.values():
        data["monster"].animate('alpha', 1, duration=0.5, delay=0.5)
        data["shadow"].animate('alpha', 1, duration=0.5, delay=0.5)

    delay = 0.5
    for y in range(13, -1, -1):
        for x in range(14):
            block = grid[x][y]
            new_color = random_color()
            block.current_color = new_color
            block.old_color = new_color
            block.texture = f"{COLORS[new_color]}.png"
            block.animate_scale(1, duration=0.8, delay=delay, curve=curve.in_out_quad)
            delay += 0.01

    matched = []
    help_flood()
    for block in matched:
        block.texture = f"{COLORS[block.current_color]}.png"

    current_color = grid[0][0].current_color
    invoke(enable_input, delay=delay + 0.8)


def update():
    global arrow_time
    global monster_bounce_time
    global monster_bounce
    if arrow.enabled:
        arrow_time += time.dt
        arrow.x = px(arrow_base_x + 12 + 12 * __import__("math").sin(arrow_time * 3.5))

    if monster_bounce is not None:
        monster_bounce_time += time.dt

        base_y = py(
            next(
                data["y"]
                for data in icons.values()
                if data["monster"] is monster_bounce
            )
        )

        monster_bounce.y = (
                base_y
                + 12 * __import__("math").sin(monster_bounce_time * 7)
        )

    for particle in particles.copy():
        particle.update_particle()

    hovered = mouse.hovered_entity
    hovered_icon = None
    for data in icons.values():
        if hovered is data["shadow"]:
            hovered_icon = data
            break

    if hovered_icon is not None and allow_click:
        icon_hovered(hovered_icon)
    else:
        if cursor_indicator is not None and cursor_indicator.enabled:
            cursor_indicator.alpha -= time.dt * 5

            if cursor_indicator.alpha <= 0:
                cursor_indicator.enabled = False

        if arrow is not None:
            arrow.texture = "assets/arrow-white.png"

        if monster_bounce is not None:
            for data in icons.values():
                if data["monster"] is monster_bounce:
                    data["monster"].y = py(data["y"])
                    break
            monster_bounce = None


def input(key):
    if key == "left mouse down":
        if game_over:
            reset_game()
            return

        hovered = mouse.hovered_entity
        for data in icons.values():
            if hovered is data["shadow"]:
                icon_clicked(data)
                return


background = create_sprite("background", 400, 300, z=-100)
grid_background = create_sprite("grid", 400, 900, z=-1000)
grid_background.enabled = False
create_grid()
help_flood()
current_color = grid[0][0].current_color
create_icons()
create_cursor()
create_arrow()
text_moves = create_text("Moves", 684, 30, size=20, alpha=0)
text_number = create_text("00", 694, 60, size=40, alpha=0)
text_message = create_text("So close!\n\nClick to\ntry again", 180, 200, size=48, alpha=0)
text_message.enabled = False
instructions = create_sprite("instructions", 400, 300, z=8)
instructions.alpha = 0
reveal_grid()
app.run()
