from ursina import application
from ursina.main import Ursina

app = Ursina()

def input(key):
    if key == "escape":
        application.quit()

app.run()
