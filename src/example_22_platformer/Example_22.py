from ursina import *

# ============================================================
# Configuration
# ============================================================

GAME_WIDTH = 800
GAME_HEIGHT = 600

GRAVITY = 900
PLAYER_SPEED = 160
JUMP_SPEED = 700


# ============================================================
# Game Objects
# ============================================================

class Platform(Entity):
    def __init__(self, position, scale, texture):
        super().__init__(
            position=position,
            scale=scale,
            model='quad',
            texture=texture,
            collider='box'
        )


class Star(Entity):
    def __init__(self, position, texture):
        super().__init__(
            position=position,
            model='quad',
            texture=texture,
            scale=(24, 24),
            collider='box'
        )

        self.base_y = position[1]
        self.bounce_speed = random.uniform(1.5, 3.0)
        self.bounce_amount = random.uniform(2, 6)
        self.active = True

        self.velocity = Vec2(0, 0)
        self.bounce_y = random.uniform(0.4, 0.8)

    def update_star(self):
        if not self.active:
            return

        self.y = (
                self.base_y
                + math.sin(time.time() * self.bounce_speed) * self.bounce_amount
        )


class Bomb(Entity):
    def __init__(self, position, texture):
        super().__init__(
            position=position,
            model='quad',
            texture=texture,
            scale=(14, 14),
            collider='box'
        )

        self.velocity = Vec2(
            random.uniform(-200, 200),
            20
        )

        self.bounce = 1.0


# ============================================================
# Player
# ============================================================

class Player(Entity):

    def __init__(self, position, texture):
        super().__init__(
            position=position,
            model='quad',
            texture=texture,
            scale=(32, 48),
            collider='box'
        )

        self.texture = texture

        self.velocity = Vec2(0, 0)

        self.bounce = 0.2

        self.on_ground = False
        self.dead = False

        # Phaser's spritesheet:
        #
        # frame 0-3 = left
        # frame 4   = idle
        # frame 5-8 = right
        #
        # We reproduce that here by changing the UV offset.
        self.frame = 4
        self.animation_timer = 0
        self.animation_frame = 0

        self.set_frame(4)

    def set_frame(self, frame):
        self.frame = frame

        # The Phaser spritesheet is assumed to be:
        #
        # 9 frames horizontally
        # each frame = 32 x 48
        #
        # Ursina can display a portion of a texture using texture_scale
        # and texture_offset.

        self.texture_scale = (1 / 9, 1)
        self.texture_offset = (frame / 9, 0)

    def animate_left(self):
        self.animation_timer += time.dt

        if self.animation_timer >= 0.1:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4

        self.set_frame(self.animation_frame)

    def animate_right(self):
        self.animation_timer += time.dt

        if self.animation_timer >= 0.1:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4

        self.set_frame(5 + self.animation_frame)

    def animate_idle(self):
        self.animation_timer = 0
        self.animation_frame = 0
        self.set_frame(4)


# ============================================================
# Main Game
# ============================================================

class PhaserPlatformerGame:

    def __init__(self):

        self.game_over = False
        self.score = 0

        # ----------------------------------------------------
        # Load assets
        # ----------------------------------------------------

        self.sky_texture = load_texture('sky.png')

        self.ground_texture = load_texture('platform.png')

        self.star_texture = load_texture('star.png')

        self.bomb_texture = load_texture('bomb.png')

        self.dude_texture = load_texture('dude.png')

        # ----------------------------------------------------
        # Background
        # ----------------------------------------------------

        self.sky = Entity(
            model='quad',
            texture=self.sky_texture,
            position=(400, 300, 10),
            scale=(800, 600)
        )

        # ----------------------------------------------------
        # Platforms
        # ----------------------------------------------------

        self.platforms = []

        # Phaser:
        #
        # create(400, 568, 'ground').setScale(2)
        #
        # Original platform is 400x32, therefore this becomes
        # 800x64.

        self.platforms.append(
            Platform(
                position=(400, 32),
                scale=(800, 64),
                texture=self.ground_texture
            )
        )

        self.platforms.append(
            Platform(
                position=(600, 200),
                scale=(400, 32),
                texture=self.ground_texture
            )
        )

        self.platforms.append(
            Platform(
                position=(50, 350),
                scale=(400, 32),
                texture=self.ground_texture
            )
        )

        self.platforms.append(
            Platform(
                position=(750, 380),
                scale=(400, 32),
                texture=self.ground_texture
            )
        )

        # ----------------------------------------------------
        # Player
        # ----------------------------------------------------

        self.player = Player(
            position=(100, 150),
            texture=self.dude_texture
        )

        # ----------------------------------------------------
        # Stars
        # ----------------------------------------------------

        self.stars = []

        for i in range(12):
            x = 12 + i * 70

            star = Star(
                position=(x, 600),
                texture=self.star_texture
            )

            self.stars.append(star)

        # ----------------------------------------------------
        # Bombs
        # ----------------------------------------------------

        self.bombs = []

        # ----------------------------------------------------
        # Score
        # ----------------------------------------------------

        self.score_text = Text(
            text='Score: 0',
            position=(-0.48, 0.43),
            origin=(0, 0),
            scale=2
        )

        # Game-over text
        self.game_over_text = Text(
            text='GAME OVER',
            origin=(0, 0),
            scale=3,
            enabled=False
        )

        # Start stars falling just like Phaser's physics group.
        for star in self.stars:
            star.velocity.y = random.uniform(-20, 0)

    # ========================================================
    # Collision helpers
    # ========================================================

    @staticmethod
    def overlaps(a, b):

        return (
                abs(a.x - b.x) < (a.scale_x + b.scale_x) / 2
                and
                abs(a.y - b.y) < (a.scale_y + b.scale_y) / 2
        )

    # ========================================================
    # Platform collision
    # ========================================================

    def move_player(self):

        player = self.player

        # ----------------------------------------------------
        # Horizontal movement
        # ----------------------------------------------------

        if held_keys['left arrow']:
            player.velocity.x = -PLAYER_SPEED
            player.animate_left()

        elif held_keys['right arrow']:
            player.velocity.x = PLAYER_SPEED
            player.animate_right()

        else:
            player.velocity.x = 0
            player.animate_idle()

        # ----------------------------------------------------
        # Jump
        # ----------------------------------------------------

        if (
                held_keys['up arrow']
                and player.on_ground
        ):
            player.velocity.y = JUMP_SPEED
            player.on_ground = False

        # ----------------------------------------------------
        # Gravity
        # ----------------------------------------------------

        player.velocity.y -= GRAVITY * time.dt

        # ----------------------------------------------------
        # Horizontal movement
        # ----------------------------------------------------

        player.x += player.velocity.x * time.dt

        # World bounds
        half_width = player.scale_x / 2

        player.x = clamp(
            player.x,
            half_width,
            GAME_WIDTH - half_width
        )

        # ----------------------------------------------------
        # Vertical movement
        # ----------------------------------------------------

        old_y = player.y

        player.y += player.velocity.y * time.dt

        player.on_ground = False

        # ----------------------------------------------------
        # Platform collision
        # ----------------------------------------------------

        for platform in self.platforms:

            platform_top = (
                    platform.y +
                    platform.scale_y / 2
            )

            platform_left = (
                    platform.x -
                    platform.scale_x / 2
            )

            platform_right = (
                    platform.x +
                    platform.scale_x / 2
            )

            player_left = (
                    player.x -
                    player.scale_x / 2
            )

            player_right = (
                    player.x +
                    player.scale_x / 2
            )

            player_bottom = (
                    player.y -
                    player.scale_y / 2
            )

            # Player is falling onto platform
            if (
                    player.velocity.y <= 0
                    and
                    old_y - player.scale_y / 2 >= platform_top - 2
                    and
                    player_bottom <= platform_top
                    and
                    player_right > platform_left
                    and
                    player_left < platform_right
            ):
                player.y = platform_top + player.scale_y / 2

                # Phaser's bounce = 0.2
                player.velocity.y = (
                        abs(player.velocity.y) * player.bounce
                )

                # Small velocities should settle
                if abs(player.velocity.y) < 50:
                    player.velocity.y = 0
                    player.on_ground = True

    # ========================================================
    # Star physics
    # ========================================================

    def update_stars(self):

        for star in self.stars:

            if not star.active:
                continue

            # Gravity
            star.velocity.y -= GRAVITY * time.dt

            star.y += star.velocity.y * time.dt

            # Platform collision
            for platform in self.platforms:

                platform_top = (
                        platform.y +
                        platform.scale_y / 2
                )

                platform_left = (
                        platform.x -
                        platform.scale_x / 2
                )

                platform_right = (
                        platform.x +
                        platform.scale_x / 2
                )

                star_left = star.x - star.scale_x / 2
                star_right = star.x + star.scale_x / 2
                star_bottom = star.y - star.scale_y / 2

                if (
                        star.velocity.y <= 0
                        and
                        star_bottom <= platform_top
                        and
                        star_right > platform_left
                        and
                        star_left < platform_right
                ):

                    star.y = platform_top + star.scale_y / 2

                    # Phaser setBounceY(0.4 - 0.8)
                    star.velocity.y = (
                            abs(star.velocity.y)
                            * star.bounce_y
                    )

                    if abs(star.velocity.y) < 20:
                        star.velocity.y = 0

    # ========================================================
    # Bomb physics
    # ========================================================

    def update_bombs(self):

        for bomb in self.bombs:

            bomb.velocity.y -= GRAVITY * time.dt

            bomb.x += bomb.velocity.x * time.dt
            bomb.y += bomb.velocity.y * time.dt

            # World bounds
            half_width = bomb.scale_x / 2

            if bomb.x <= half_width:
                bomb.x = half_width
                bomb.velocity.x *= -1

            elif bomb.x >= GAME_WIDTH - half_width:
                bomb.x = GAME_WIDTH - half_width
                bomb.velocity.x *= -1

            # Platform collision
            for platform in self.platforms:

                platform_top = (
                        platform.y +
                        platform.scale_y / 2
                )

                platform_left = (
                        platform.x -
                        platform.scale_x / 2
                )

                platform_right = (
                        platform.x +
                        platform.scale_x / 2
                )

                bomb_left = bomb.x - bomb.scale_x / 2
                bomb_right = bomb.x + bomb.scale_x / 2
                bomb_bottom = bomb.y - bomb.scale_y / 2

                if (
                        bomb.velocity.y <= 0
                        and
                        bomb_bottom <= platform_top
                        and
                        bomb_right > platform_left
                        and
                        bomb_left < platform_right
                ):

                    bomb.y = (
                            platform_top +
                            bomb.scale_y / 2
                    )

                    bomb.velocity.y = (
                            abs(bomb.velocity.y)
                            * bomb.bounce
                    )

                    # Keep bomb moving horizontally
                    if abs(bomb.velocity.x) < 10:
                        bomb.velocity.x = random.choice(
                            [-100, 100]
                        )

    # ========================================================
    # Star collection
    # ========================================================

    def collect_star(self, star):

        star.active = False
        star.enabled = False

        self.score += 10

        self.score_text.text = f'Score: {self.score}'

        # Are all stars collected?
        active_stars = [
            s for s in self.stars
            if s.active
        ]

        if len(active_stars) == 0:

            # ------------------------------------------------
            # New batch of stars
            # ------------------------------------------------

            for star in self.stars:
                star.active = True
                star.enabled = True

                star.x = star.x
                star.y = 600

                star.velocity.y = 0
                star.bounce_y = random.uniform(
                    0.4,
                    0.8
                )

            # ------------------------------------------------
            # Spawn bomb on opposite side of player
            # ------------------------------------------------

            if self.player.x < 400:

                x = random.uniform(400, 800)

            else:

                x = random.uniform(0, 400)

            bomb = Bomb(
                position=(x, 584),
                texture=self.bomb_texture
            )

            self.bombs.append(bomb)

    # ========================================================
    # Check star collisions
    # ========================================================

    def check_star_collisions(self):

        for star in self.stars:

            if not star.active:
                continue

            if self.overlaps(
                    self.player,
                    star
            ):
                self.collect_star(star)

    # ========================================================
    # Check bomb collisions
    # ========================================================

    def check_bomb_collisions(self):

        for bomb in self.bombs:

            if self.overlaps(
                    self.player,
                    bomb
            ):
                self.hit_bomb(bomb)
                return

    # ========================================================
    # Hit bomb
    # ========================================================

    def hit_bomb(self, bomb):

        if self.game_over:
            return

        self.game_over = True

        # Phaser:
        #
        # this.physics.pause();
        # player.setTint(0xff0000);
        #
        # Here we stop player physics and tint the player red.

        self.player.texture = self.dude_texture
        self.player.color = color.red

        self.game_over_text.enabled = True

    # ========================================================
    # Main update
    # ========================================================

    def update(self):

        if self.game_over:
            return

        self.move_player()

        self.update_stars()

        self.update_bombs()

        self.check_star_collisions()

        self.check_bomb_collisions()


# ============================================================
# Ursina initialization
# ============================================================

app = Ursina()

window.title = 'Phaser Platformer - Ursina'
window.size = (GAME_WIDTH, GAME_HEIGHT)

# Don't stretch the game objects independently.
window.color = color.black

# Set camera to orthographic for 2D game
camera.orthographic = True
camera.fov = 600  # Height of the view in world units

# Center camera on game world (game uses 0,0 at bottom-left like Phaser)
camera.position = (400, 300, -10)

game = PhaserPlatformerGame()


# Ursina calls this automatically every frame.
def update():
    game.update()


app.run()
