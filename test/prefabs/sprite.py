from ursina import Ursina, Sprite, camera, Texture

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    camera.fov = 1
    Sprite.ppu = 16
    Texture.default_filtering = None
    s = Sprite('brick', filtering=False)
    app.run()
