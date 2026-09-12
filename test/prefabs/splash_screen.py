from ursina import Ursina, Vec2, color, window
from ursina.prefabs.splash_screen import UrsinaSplashScreen

if __name__ == '__main__':
    app = Ursina(size=Vec2(1920,1080), )
    window.color = color.black
    ursina_splash_screen = UrsinaSplashScreen()
    app.run()
