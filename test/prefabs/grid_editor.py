from PIL import Image
from ursina import Ursina, Texture, scene, load_texture, camera, EditorCamera
from ursina.prefabs.grid_editor import PixelEditor

if __name__ == '__main__':

    '''
    pixel editor example, it's basically a drawing tool.
    can be useful for level editors and stuff like that.
    Here we create a new texture, but can also give it an existing texture to modify.
    '''
    app = Ursina()
    t = Texture(Image.new(mode="RGBA", size=(32, 32), color=(0, 0, 0, 1)))
    editor = PixelEditor(parent=scene, texture=load_texture("test_tileset"), scale=10)
    camera.orthographic = True
    camera.fov = 15
    EditorCamera(rotation_speed=0)
    app.run()
