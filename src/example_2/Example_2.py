from random import choice, randint

from ursina import (Ursina, window, camera, color, Entity, Text, Audio, time, destroy, BoxCollider, Vec3)

GAME_WIDTH = 800
GAME_HEIGHT = 400
GROUND_Y = -2.0
PLAYER_X = -6.0
GRAVITY = 35
JUMP_SPEED = 15
OBSTACLE_SPEED = 7
SPAWN_INTERVAL = 1.5
PLAYER_ANIMATION_SPEED = 0.1
OBSTACLE_ANIMATION_SPEED = 0.1

app = Ursina()
window.title = "Pixel Runner"
window.borderless = False
camera.orthographic = True
camera.fov = 18

game_active = False
score = 0
game_time = 0
spawn_timer = 0
obstacles = []

sky = Entity(model='quad', texture='assets/graphics/Sky.png', scale=(55, 30), position=(0, 0, 10))
ground = Entity(model='quad', texture='assets/graphics/ground.png', scale=(55, 15), position=(0, -7.5, 0))


class Player(Entity):

    def __init__(self):
        super().__init__(
            model='quad',
            texture='assets/graphics/Player/player_walk_1.png',
            scale=(1.5, 2),
            position=(PLAYER_X, GROUND_Y, -1),
            collider='box'
        )

        self.collider = BoxCollider(self, center=Vec3(0, 0, 0), size=Vec3(0.7, 0.85, 1))
        self.walk_frames = ['assets/graphics/Player/player_walk_1.png', 'assets/graphics/Player/player_walk_2.png']
        self.jump_frame = 'assets/graphics/Player/jump.png'
        self.animation_index = 0
        self.animation_timer = 0
        self.velocity_y = 0
        self.is_grounded = True

    def jump(self):
        if self.is_grounded:
            self.velocity_y = JUMP_SPEED
            self.is_grounded = False
            if jump_sound:
                jump_sound.play()

    def update(self):
        if not game_active:
            return

        self.velocity_y -= GRAVITY * time.dt
        self.y += self.velocity_y * time.dt
        if self.y <= GROUND_Y:
            self.y = GROUND_Y
            self.velocity_y = 0
            self.is_grounded = True

        if not self.is_grounded:
            self.texture = self.jump_frame
        else:
            self.animation_timer += time.dt
            if self.animation_timer >= PLAYER_ANIMATION_SPEED:
                self.animation_timer = 0
                self.animation_index += 1
                if self.animation_index >= len(self.walk_frames):
                    self.animation_index = 0
                self.texture = self.walk_frames[self.animation_index]


player = Player()


class Obstacle(Entity):
    def __init__(self, obstacle_type):

        if obstacle_type == 'fly':
            frames = ['assets/graphics/Fly/Fly1.png', 'assets/graphics/Fly/Fly2.png']
            y_position = -0.3
            scale = (1.4, 1.2)
        else:
            frames = ['assets/graphics/snail/snail1.png', 'assets/graphics/snail/snail2.png']
            y_position = GROUND_Y
            scale = (1.4, 1.0)

        super().__init__(
            model='quad',
            texture=frames[0],
            scale=scale,
            position=(randint(11, 14), y_position, -1), collider='box')

        if obstacle_type == 'fly':
            self.collider = BoxCollider(self, center=Vec3(0, 0, 0), size=Vec3(0.7, 0.6, 1))
        else:
            self.collider = BoxCollider(self, center=Vec3(0, 0, 0), size=Vec3(0.75, 0.8, 1))

        self.obstacle_type = obstacle_type
        self.frames = frames
        self.animation_index = 0
        self.animation_timer = 0

    def update(self):

        if not game_active:
            return
        self.x -= OBSTACLE_SPEED * time.dt
        self.animation_timer += time.dt
        if self.animation_timer >= OBSTACLE_ANIMATION_SPEED:
            self.animation_timer = 0
            self.animation_index += 1
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.texture = self.frames[self.animation_index]

        if self.x < -12:
            if self in obstacles:
                obstacles.remove(self)
            destroy(self)


score_text = Text(text='Score: 0', origin=(0, 0), position=(0, 0.42), scale=1.5, color=color.rgb(64, 64, 64))
title_text = Text(text='Pixel Runner', origin=(0, 0), position=(0, 0.25), scale=2, color=color.rgb(111, 196, 169))
message_text = Text(text='Press SPACE to run', origin=(0, 0), position=(0, -0.35), scale=1.3, color=color.rgb(111, 196, 169))
game_over_text = Text(text='', origin=(0, 0), position=(0, -0.35), scale=1.3, color=color.rgb(111, 196, 169))
player_stand = Entity(model='quad', texture='assets/graphics/Player/player_stand.png', scale=(2, 2), position=(0, -0.1, -1))
player_stand.enabled = True
jump_sound = None
music = None

try:
    jump_sound = Audio("assets/audio/jump.wav", autoplay=False)
    jump_sound.volume = 0.5
except Exception as e:
    print("Could not load jump sound:", e)

try:
    music = Audio("assets/audio/music.wav", autoplay=False, loop=True)
    music.volume = 0.15

except Exception as e:
    print("Could not load music:", e)


def start_game():
    global game_active
    global score
    global game_time
    global spawn_timer

    game_active = True
    score = 0
    game_time = 0
    spawn_timer = 0

    player.position = (PLAYER_X, GROUND_Y, -1)
    player.velocity_y = 0
    player.is_grounded = True
    player.animation_index = 0

    for obstacle in obstacles[:]:
        destroy(obstacle)

    obstacles.clear()
    sky.enabled = True
    ground.enabled = True
    player.enabled = True
    title_text.enabled = False
    message_text.enabled = False
    game_over_text.enabled = False
    player_stand.enabled = False
    score_text.enabled = True
    if music:
        music.play()


def game_over():
    global game_active
    game_active = False

    if music:
        music.stop()

    game_over_text.text = f'Your score: {score}\nPress SPACE to run again'
    game_over_text.enabled = True
    title_text.enabled = True
    player_stand.enabled = True
    score_text.enabled = False
    sky.enabled = False
    ground.enabled = False
    player.enabled = False

    for obstacle in obstacles[:]:
        destroy(obstacle)
    obstacles.clear()


def spawn_obstacle():
    obstacle_type = choice(['fly', 'snail', 'snail', 'snail'])
    obstacle = Obstacle(obstacle_type)
    obstacles.append(obstacle)


def _aabb_overlap(a, b):
    a_col = a.collider
    b_col = b.collider
    a_hx = abs(a.scale_x * a_col.size.x) / 2
    a_hy = abs(a.scale_y * a_col.size.y) / 2
    b_hx = abs(b.scale_x * b_col.size.x) / 2
    b_hy = abs(b.scale_y * b_col.size.y) / 2

    ax = a.world_x + a_col.center.x * a.scale_x
    ay = a.world_y + a_col.center.y * a.scale_y
    bx = b.world_x + b_col.center.x * b.scale_x
    by = b.world_y + b_col.center.y * b.scale_y

    return abs(ax - bx) < (a_hx + b_hx) and abs(ay - by) < (a_hy + b_hy)


def check_collision():
    for obstacle in obstacles:
        if _aabb_overlap(player, obstacle):
            return True
    return False


def input(key):
    if key == 'space':
        if not game_active:
            start_game()
        else:
            player.jump()


def update():
    global game_time
    global score
    global spawn_timer

    if not game_active:
        return

    game_time += time.dt
    score = int(game_time)
    score_text.text = f'Score: {score}'
    spawn_timer += time.dt

    if spawn_timer >= SPAWN_INTERVAL:
        spawn_timer = 0
        spawn_obstacle()
    if check_collision():
        game_over()


score_text.enabled = False
game_over_text.enabled = False
title_text.enabled = True
message_text.enabled = True
player_stand.enabled = True
sky.enabled = False
ground.enabled = False
player.enabled = False

app.run()
