import random
from ursina import Ursina, camera, window, color, Entity, Texture, held_keys, time

GAME_WIDTH = 640
GAME_HEIGHT = 480
GRID_WIDTH = 40
GRID_HEIGHT = 30
CELL_SIZE = 16
app = Ursina(title="Snake", size=(GAME_WIDTH, GAME_HEIGHT), forced_aspect_ratio=GAME_WIDTH / GAME_HEIGHT, )
camera.orthographic = True
camera.fov = GAME_HEIGHT
window.color = color.rgb(191, 204, 0)
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

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

class Food:
    def __init__(self, x, y):
        self.entity = create_sprite("food", x * CELL_SIZE, y * CELL_SIZE, z=1)
        self.total = 0

    @property
    def x(self):
        return self.entity.x

    @property
    def y(self):
        return self.entity.y

    def set_position(self, x, y):
        self.entity.x = px(x * CELL_SIZE)
        self.entity.y = py(y * CELL_SIZE)

    def eat(self):
        self.total += 1

class Snake:
    def __init__(self, x, y):
        self.head_x = x
        self.head_y = y
        self.body = []
        head = create_sprite("body", x * CELL_SIZE, y * CELL_SIZE, z=2)
        self.body.append({"entity": head, "x": x, "y": y})
        self.alive = True
        self.speed = 100
        self.move_time = 0
        self.tail_x = x
        self.tail_y = y
        self.heading = RIGHT
        self.direction = RIGHT

    @property
    def head(self):
        return self.body[0]["entity"]

    def face_left(self):
        if self.direction == UP or self.direction == DOWN:
            self.heading = LEFT

    def face_right(self):
        if self.direction == UP or self.direction == DOWN:
            self.heading = RIGHT

    def face_up(self):
        if self.direction == LEFT or self.direction == RIGHT:
            self.heading = UP

    def face_down(self):
        if self.direction == LEFT or self.direction == RIGHT:
            self.heading = DOWN

    def update(self, current_time):
        if current_time >= self.move_time:
            return self.move(current_time)
        return None

    def move(self, current_time):
        if self.heading == LEFT:
            self.head_x = (self.head_x - 1) % GRID_WIDTH
        elif self.heading == RIGHT:
            self.head_x = (self.head_x + 1) % GRID_WIDTH
        elif self.heading == UP:
            self.head_y = (self.head_y - 1) % GRID_HEIGHT
        elif self.heading == DOWN:
            self.head_y = (self.head_y + 1) % GRID_HEIGHT
        self.direction = self.heading
        self.tail_x = self.body[-1]["x"]
        self.tail_y = self.body[-1]["y"]

        for index in range(len(self.body) - 1, 0, -1):
            previous = self.body[index - 1]
            self.body[index]["x"] = previous["x"]
            self.body[index]["y"] = previous["y"]
            self.body[index]["entity"].x = px(previous["x"] * CELL_SIZE)
            self.body[index]["entity"].y = py(previous["y"] * CELL_SIZE)

        self.body[0]["x"] = self.head_x
        self.body[0]["y"] = self.head_y
        self.head.x = px(self.head_x * CELL_SIZE)
        self.head.y = py(self.head_y * CELL_SIZE)

        for segment in self.body[1:]:
            if (segment["x"] == self.head_x and segment["y"] == self.head_y):
                print("dead")
                self.alive = False
                return False

        self.move_time = current_time + self.speed
        return True

    def grow(self):
        new_part = create_sprite("body", self.tail_x * CELL_SIZE, self.tail_y * CELL_SIZE, z=2)
        self.body.append({"entity": new_part, "x": self.tail_x, "y": self.tail_y})

    def collide_with_food(self, food):
        if (self.head_x == int(to_phaser_x(food.entity.x) / CELL_SIZE)
                and
                self.head_y == int(to_phaser_y(food.entity.y) / CELL_SIZE)
        ):

            self.grow()
            food.eat()

            if self.speed > 20 and food.total % 5 == 0:
                self.speed -= 5
            return True
        return False

    def update_grid(self, grid):
        for segment in self.body:
            x = segment["x"]
            y = segment["y"]

            if 0 <= y < len(grid) and 0 <= x < len(grid[y]):
                grid[y][x] = False
        return grid

snake = None
food = None
game_time = 0.0

def create():
    global snake
    global food
    food = Food(3, 4)
    snake = Snake(8, 8)

def reposition_food():
    test_grid = []

    for y in range(GRID_HEIGHT):
        row = []
        for x in range(GRID_WIDTH):
            row.append(True)
        test_grid.append(row)

    snake.update_grid(test_grid)
    valid_locations = []

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):

            if test_grid[y][x]:
                valid_locations.append((x, y))

    if len(valid_locations) == 0:
        return False

    x, y = random.choice(valid_locations)
    food.set_position(x, y)
    return True

def update_controls():
    if held_keys["left arrow"]:
        snake.face_left()
    elif held_keys["right arrow"]:
        snake.face_right()
    elif held_keys["up arrow"]:
        snake.face_up()
    elif held_keys["down arrow"]:
        snake.face_down()

def update():
    global game_time
    if not snake.alive:
        return

    game_time += time.dt * 1000
    update_controls()

    if snake.update(game_time):
        if snake.collide_with_food(food):
            reposition_food()

create()
app.run()
