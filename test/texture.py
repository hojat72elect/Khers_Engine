from ursina import texture_importer, Ursina, Entity, color, application,Array2D, enumerate_2d, Texture, EditorCamera
from pathlib import Path

if __name__ == "__main__":
    app = Ursina()
    """
        The Texture class rarely used manually but usually instantiated
        when assigning a texture to an Entity
        texture = Texture(path / PIL.Image / panda3d.core.Texture)

        A texture file can be a .png, .jpg or .psd.
        If it's a .psd it and no compressed version exists, it will compress it automatically.
    """
    e = Entity(model="quad", texture="test_tileset")
    e.texture.set_pixel(0, 2, color.blue)
    e.texture.apply()

    application.asset_folder = Path(r"C:\sync\high resolution images")
    e:Entity = Entity(model="quad")

    def input(key):
        if key == "a":
            e.texture = "tesla_city"
        if key == "space":
            t = e.texture._texture
            e.texture = None
            t.releaseAll()
            t.clearRamImage()
        if key == "p":
            for key, value in texture_importer.imported_textures.items():
                print(key, value)

    e.texture = "test_tileset"
    e.texture.apply()
    pixels = e.texture.pixels
    new_grid = Array2D(width=pixels.width, height=pixels.height)
    print("w:", pixels.width, "h:", pixels.height)
    for (x, y), value in enumerate_2d(pixels):
        new_grid[x][y] = int(color.rgba32(*value).v > 0.5)

    texture_from_base64_string = Entity(
        model="cube",
        y=1.5,
        scale=1,
        texture=Texture("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAIAAAAmkwkpAAAAJ0lEQVR4nGK5d/gdAwODArcEkGRiQAKMmut0gdTX/YroMoAAAAD//8caBbV8Qu6pAAAAAElFTkSuQmCC")
    )
    EditorCamera()
    app.run()
