from ursina import Ursina, application

app = Ursina()


def input(key):
    if key == "escape":
        application.quit()


app.run()
