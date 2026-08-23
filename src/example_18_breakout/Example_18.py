from ursina import Ursina, application

GAME_WIDTH = 800
GAME_HEIGHT = 600

app = Ursina(title="Breakout", size=(GAME_WIDTH, GAME_HEIGHT), forced_aspect_ratio=GAME_WIDTH / GAME_HEIGHT, )


def input(key):
    if key == 'escape':
        application.quit()


app.run()
