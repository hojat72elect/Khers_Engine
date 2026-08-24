from ursina import *

# ============================================================
# Configuration
# ============================================================

GAME_WIDTH = 549
GAME_HEIGHT = 480

# ============================================================
# Ursina application
# ============================================================

app = Ursina(
    title="Card Memory Game",
    borderless=False,
)

window.title = "Card Memory Game"
window.color = color.rgb(25, 42, 86)
window.fps_counter.enabled = False

# Phaser's game is essentially a 549x480 2D game.
# Using an orthographic camera with a 480-unit vertical field
# gives us convenient pixel-like coordinates.
camera.orthographic = True
camera.fov = GAME_HEIGHT
camera.position = (0, 0, -100)

# Keep nearest filtering for the pixel-art look.
Texture.default_filtering = None


# ============================================================
# Helpers
# ============================================================


def px_to_world(x, y):
    """
    Convert Phaser-style top-left pixel coordinates into
    Ursina's centered coordinate system.
    """
    world_x = x - GAME_WIDTH / 2
    world_y = GAME_HEIGHT / 2 - y
    return world_x, world_y


def wait(duration, callback):
    """Small helper around Ursina's invoke()."""
    invoke(callback, delay=duration)


# ============================================================
# Audio
# ============================================================

sounds = {
    "theme-song": Audio(
        "audio/fat-caps-audionatix.mp3",
        autoplay=False,
        loop=True,
        volume=0.5,
    ),

    "whoosh": Audio(
        "audio/whoosh.mp3",
        autoplay=False,
        volume=1.0,
    ),

    "card-flip": Audio(
        "audio/card-flip.mp3",
        autoplay=False,
        volume=1.0,
    ),

    "card-match": Audio(
        "audio/card-match.mp3",
        autoplay=False,
        volume=1.0,
    ),

    "card-mismatch": Audio(
        "audio/card-mismatch.mp3",
        autoplay=False,
        volume=1.0,
    ),

    "card-slide": Audio(
        "audio/card-slide.mp3",
        autoplay=False,
        volume=1.0,
    ),

    "victory": Audio(
        "audio/victory.mp3",
        autoplay=False,
        volume=1.0,
    ),
}

sound_enabled = True


def play_sound(name, volume=1.0):
    """Play a sound while respecting the volume toggle."""
    if not sound_enabled:
        return

    sound = sounds.get(name)

    if sound is None:
        return

    sound.volume = volume
    sound.play()


# ============================================================
# Game state
# ============================================================

CARD_NAMES = [
    "card-0",
    "card-1",
    "card-2",
    "card-3",
    "card-4",
    "card-5",
]

CARD_WIDTH = 98
CARD_HEIGHT = 128

GRID_X = 113
GRID_Y = 102

PADDING_X = 10
PADDING_Y = 10

cards = []
hearts = []

card_opened = None

can_move = False
lives = 10

game_started = False
game_finished = False
game_over = False
game_won = False

# ============================================================
# Camera shake
# ============================================================

camera_shake_time = 0
camera_shake_strength = 0


def shake_camera(duration=0.6, strength=3):
    global camera_shake_time
    global camera_shake_strength

    camera_shake_time = duration
    camera_shake_strength = strength


def update_camera_shake():
    global camera_shake_time

    if camera_shake_time > 0:
        camera_shake_time -= time.dt

        camera.x = random.uniform(
            -camera_shake_strength,
            camera_shake_strength,
        )

        camera.y = random.uniform(
            -camera_shake_strength,
            camera_shake_strength,
        )
    else:
        camera.x = 0
        camera.y = 0


# ============================================================
# Card class
# ============================================================

class MemoryCard:
    def __init__(self, x, y, card_name, start_y=None):
        self.card_name = card_name

        self.is_flipping = False
        self.destroyed = False
        self.face_up = False

        if start_y is None:
            start_y = y

        world_x, world_y = px_to_world(x, start_y)

        self.target_position = Vec3(
            px_to_world(x, y)[0],
            px_to_world(x, y)[1],
            0,
        )

        self.entity = Entity(
            model="quad",
            texture="cards/card-back.png",
            position=(world_x, world_y, 0),
            scale=(CARD_WIDTH, CARD_HEIGHT),
            collider="box",
        )

        self.entity.name = card_name
        self.entity.card = self

        # Start above the screen.
        self.entity.y = px_to_world(x, -150)[1]

        # Flip animation state.
        self.flip_start_rotation = 180
        self.flip_target_rotation = 0
        self.flip_elapsed = 0
        self.flip_duration = 0.5

        # Entry animation.
        self.entry_start_y = self.entity.y
        self.entry_elapsed = 0
        self.entry_duration = 0.8
        self.entry_delay = 0

    # --------------------------------------------------------
    # Entry animation
    # --------------------------------------------------------

    def start_entry_animation(self, delay):
        self.entry_delay = delay

    def update(self):
        # ---------------------------------------------
        # Entry animation
        # ---------------------------------------------

        if self.entry_delay > 0:
            self.entry_delay -= time.dt

        elif self.entity.y != self.target_position.y and self.entry_elapsed < self.entry_duration:
            self.entry_elapsed += time.dt

            t = min(
                self.entry_elapsed / self.entry_duration,
                1.0,
            )

            # Expo-like easing.
            eased = 1 - pow(2, -10 * t)

            self.entity.y = lerp(
                self.entry_start_y,
                self.target_position.y,
                eased,
            )

            if random.random() < 0.025:
                play_sound("card-slide", 1.2)

        # ---------------------------------------------
        # Flip animation
        # ---------------------------------------------

        if self.is_flipping:
            self.flip_elapsed += time.dt

            t = min(
                self.flip_elapsed / self.flip_duration,
                1.0,
            )

            # Exponential ease-out.
            eased = 1 - pow(2, -10 * t)

            rotation = lerp(
                self.flip_start_rotation,
                self.flip_target_rotation,
                eased,
            )

            self.entity.rotation_y = rotation

            # Swap texture around the midpoint.
            if rotation < 90 and not self.face_up:
                self.entity.texture = f"cards/{self.card_name}.png"
                self.face_up = True

            elif rotation >= 90 and self.face_up:
                self.entity.texture = "cards/card-back.png"
                self.face_up = False

            # Finish.
            if t >= 1:
                self.entity.rotation_y = self.flip_target_rotation
                self.is_flipping = False

    # --------------------------------------------------------
    # Flip
    # --------------------------------------------------------

    def flip(self, callback=None):
        if self.is_flipping or self.destroyed:
            return

        self.is_flipping = True
        self.flip_elapsed = 0

        play_sound("card-flip")

        if self.face_up:
            self.flip_start_rotation = 0
            self.flip_target_rotation = 180
        else:
            self.flip_start_rotation = 180
            self.flip_target_rotation = 0

        # Small scale bounce.
        original_scale = Vec3(
            CARD_WIDTH,
            CARD_HEIGHT,
            1,
        )

        self.entity.animate_scale(
            original_scale * 1.1,
            duration=0.2,
            curve=curve.in_expo,
        )

        self.entity.animate_scale(
            original_scale,
            duration=0.3,
            delay=0.2,
            curve=curve.out_expo,
        )

        def finish():
            if callback:
                callback()

        invoke(finish, delay=self.flip_duration)

    # --------------------------------------------------------
    # Destroy card
    # --------------------------------------------------------

    def destroy(self):
        if self.destroyed:
            return

        self.destroyed = True

        self.entity.animate_y(
            self.entity.y - 1000,
            duration=0.5,
            curve=curve.in_elastic,
        )

        invoke(
            self.entity.disable,
            delay=0.5,
        )


# ============================================================
# Background
# ============================================================

background_x, background_y = px_to_world(50, 25)

background = Entity(
    model="quad",
    texture="background.png",
    position=(background_x, background_y, 10),
    scale=(GAME_WIDTH, GAME_HEIGHT),
)

# ============================================================
# Volume button
# ============================================================

volume_x, volume_y = px_to_world(25, 25)

volume_button = Entity(
    model="quad",
    texture="ui/volume-icon.png",
    position=(volume_x, volume_y, -10),
    scale=(40, 40),
    collider="box",
)


def toggle_volume():
    global sound_enabled

    sound_enabled = not sound_enabled

    if sound_enabled:
        volume_button.texture = "ui/volume-icon.png"

        for sound in sounds.values():
            sound.volume = 1

        if game_started and not sounds["theme-song"].playing:
            sounds["theme-song"].play()
    else:
        volume_button.texture = "ui/volume-icon_off.png"

        for sound in sounds.values():
            sound.volume = 0


volume_button.on_click = toggle_volume

# ============================================================
# Text elements
# ============================================================

title_text = Text(
    text="Memory Card Game\nClick to Play",
    origin=(0, 0),
    position=(0, 20),
    scale=3,
    color=color.rgb(140, 122, 230),
    z=-20,
)

title_text_entity = title_text

winner_text = Text(
    text="YOU WIN",
    origin=(0, 0),
    position=(0, -1000),
    scale=3,
    color=color.rgb(140, 122, 230),
    z=-20,
)

game_over_text = Text(
    text="GAME OVER\nClick to restart",
    origin=(0, 0),
    position=(0, -1000),
    scale=3,
    color=color.red,
    z=-20,
)


# ============================================================
# Hearts
# ============================================================

def create_hearts():
    global hearts

    hearts = []

    for i in range(lives):
        heart_x, heart_y = px_to_world(
            140 + 30 * i,
            20,
        )

        heart = Entity(
            model="quad",
            texture="ui/heart.png",
            position=(1000, heart_y, -5),
            scale=(32, 32),
        )

        hearts.append(heart)

        heart.animate_x(
            heart_x,
            duration=1,
            delay=1 + i * 0.2,
            curve=curve.in_out_expo,
        )


# ============================================================
# Card grid
# ============================================================

def create_grid_cards():
    global cards

    shuffled_names = CARD_NAMES + CARD_NAMES
    random.shuffle(shuffled_names)

    cards = []

    for index, name in enumerate(shuffled_names):
        column = index % 4
        row = index // 4

        x = GRID_X + (CARD_WIDTH + PADDING_X) * column
        y = GRID_Y + (CARD_HEIGHT + PADDING_Y) * row

        card = MemoryCard(
            x=x,
            y=y,
            card_name=name,
            start_y=-100,
        )

        card.start_entry_animation(
            index * 0.1
        )

        cards.append(card)


# ============================================================
# Card interaction
# ============================================================

def card_clicked(card):
    global card_opened
    global can_move
    global lives

    if not game_started:
        return

    if game_finished:
        return

    if not can_move:
        return

    if card.destroyed:
        return

    if card.is_flipping:
        return

    if card not in cards:
        return

    can_move = False

    # ---------------------------------------------
    # There is already an open card.
    # ---------------------------------------------

    if card_opened is not None:

        # Same card clicked twice.
        if card_opened is card:
            can_move = True
            return

        def finish_second_card():
            global card_opened
            global can_move
            global lives

            # -------------------------------------
            # MATCH
            # -------------------------------------

            if card_opened.card_name == card.card_name:

                play_sound("card-match")

                opened = card_opened

                opened.destroy()
                card.destroy()

                if opened in cards:
                    cards.remove(opened)

                if card in cards:
                    cards.remove(card)

                card_opened = None
                can_move = True

                # WIN
                if len(cards) == 0:
                    win_game()

            # -------------------------------------
            # MISMATCH
            # -------------------------------------

            else:
                play_sound("card-mismatch")

                shake_camera(
                    duration=0.6,
                    strength=3,
                )

                remove_life()

                current_opened = card_opened

                card.flip()

                current_opened.flip(
                    callback=after_mismatch
                )

        def after_mismatch():
            global card_opened
            global can_move

            card_opened = None

            if lives > 0:
                can_move = True
            else:
                can_move = False
                lose_game()

        card.flip(
            callback=finish_second_card
        )

    # ---------------------------------------------
    # First card
    # ---------------------------------------------

    else:

        def first_card_finished():
            global can_move
            can_move = True

        card.flip(
            callback=first_card_finished
        )

        card_opened = card


# ============================================================
# Connect card clicks
# ============================================================

def connect_card_click(card):
    card.entity.on_click = Func(
        card_clicked,
        card,
    )


# ============================================================
# Remove life
# ============================================================

def remove_life():
    global lives

    if lives <= 0:
        return

    if hearts:
        last_heart = hearts[-1]

        last_heart.animate_y(
            last_heart.y + 1000,
            duration=1,
            curve=curve.in_out_expo,
        )

        invoke(
            last_heart.disable,
            delay=1,
        )

        hearts.pop()

    lives -= 1


# ============================================================
# Start game
# ============================================================

def start_game():
    global game_started
    global can_move

    if game_started:
        return

    game_started = True

    play_sound("whoosh", 1.3)

    # Animate title away.
    title_text.animate_y(
        1000,
        duration=0.8,
        curve=curve.in_bounce,
    )

    def begin():
        global can_move

        if sound_enabled and not sounds["theme-song"].playing:
            sounds["theme-song"].play()

        title_click_area.enabled = False
        create_hearts()
        create_grid_cards()

        for card in cards:
            connect_card_click(card)

        # Phaser waits approximately 200ms per card.
        invoke(
            enable_game,
            delay=2.4,
        )

    invoke(begin, delay=0.8)


def enable_game():
    global can_move
    can_move = True


# ============================================================
# Win
# ============================================================

def win_game():
    global game_finished
    global game_won
    global can_move

    if game_finished:
        return

    game_finished = True
    game_won = True
    can_move = False

    play_sound("whoosh", 1.3)
    play_sound("victory")

    winner_text.y = -1000

    winner_text.animate_y(
        0,
        duration=0.8,
        curve=curve.out_bounce,
    )


# ============================================================
# Game over
# ============================================================

def lose_game():
    global game_finished
    global game_over
    global can_move

    if game_finished:
        return

    game_finished = True
    game_over = True
    can_move = False

    play_sound("whoosh", 1.3)

    game_over_text.y = -1000

    game_over_text.animate_y(
        0,
        duration=0.8,
        curve=curve.out_bounce,
    )


# ============================================================
# Restart
# ============================================================

def restart_game():
    global cards
    global hearts
    global card_opened
    global can_move
    global lives
    global game_started
    global game_finished
    global game_over
    global game_won

    play_sound("whoosh", 1.3)

    can_move = False

    # Destroy cards.
    for index, card in enumerate(reversed(cards)):
        if not card.destroyed:
            card.entity.animate_y(
                card.entity.y - 1000,
                duration=0.5,
                delay=index * 0.1,
                curve=curve.in_out_expo,
            )

            invoke(
                card.entity.disable,
                delay=0.5 + index * 0.1,
            )

    # Remove hearts.
    for heart in hearts:
        heart.animate_x(
            1000,
            duration=0.5,
        )

        invoke(
            heart.disable,
            delay=0.5,
        )

    def restart():
        global cards
        global hearts
        global card_opened
        global can_move
        global lives
        global game_started
        global game_finished
        global game_over
        global game_won

        cards = []
        hearts = []

        card_opened = None

        lives = 10

        game_started = False
        game_finished = False
        game_over = False
        game_won = False

        winner_text.y = -1000
        game_over_text.y = -1000

        title_text.text = "Memory Card Game\nClick to Play"

        title_text.y = 20
        title_text.alpha = 1

        # Re-enable volume button and title click area.
        volume_button.enabled = True
        title_click_area.enabled = True

    invoke(
        restart,
        delay=max(
            1.0,
            0.5 + len(cards) * 0.1,
        ),
    )


# ============================================================
# Winner / game-over click handlers
# ============================================================

def click_winner():
    if not game_won:
        return

    restart_game()


def click_game_over():
    if not game_over:
        return

    restart_game()


winner_click_area = Entity(
    model="quad",
    position=(0, 0, -30),
    scale=(GAME_WIDTH, 150),
    collider="box",
    color=color.clear,
)

winner_click_area.enabled = False
winner_click_area.on_click = click_winner

game_over_click_area = Entity(
    model="quad",
    position=(0, 0, -30),
    scale=(GAME_WIDTH, 180),
    collider="box",
    color=color.clear,
)

game_over_click_area.enabled = False
game_over_click_area.on_click = click_game_over

# ============================================================
# Title interaction
# ============================================================

title_click_area = Entity(
    model="quad",
    position=(0, 20, -30),
    scale=(450, 130),
    collider="box",
    color=color.clear,
)


def title_hover():
    mouse.cursor = "hand"


def title_click():
    start_game()


title_click_area.on_click = title_click


# ============================================================
# Global input
# ============================================================

def input(key):
    if key == "escape":
        application.quit()

    # Start game with Enter or Space as an extra convenience.
    if key in ("space", "enter"):
        if not game_started:
            start_game()

    if key == "r":
        if game_finished:
            restart_game()


# ============================================================
# Update
# ============================================================

def update():
    update_camera_shake()

    # Update cards.
    for card in cards:
        if not card.destroyed:
            card.update()

    # Mouse cursor.
    if mouse.hovered_entity is not None:

        if (
                mouse.hovered_entity in
                [card.entity for card in cards]
        ):
            mouse.cursor = "hand"

        elif mouse.hovered_entity in (
                title_click_area,
                volume_button,
                winner_click_area,
                game_over_click_area,
        ):
            mouse.cursor = "hand"

        else:
            mouse.cursor = "arrow"

    else:
        mouse.cursor = "arrow"

    # Enable/disable overlay click areas.
    winner_click_area.enabled = game_won
    game_over_click_area.enabled = game_over

    # Make sure the volume button remains available.
    volume_button.enabled = True


# ============================================================
# Start
# ============================================================

app.run()
