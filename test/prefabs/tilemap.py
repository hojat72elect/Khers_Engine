from ursina import Ursina, EditorCamera, camera, Text, Vec2, window, scene
from ursina.prefabs.tilemap import Tilemap

if __name__ == '__main__':
    app = Ursina()
    EditorCamera(rotation_speed=0)
    tilemap = Tilemap('tilemap_test_level', tileset='test_tileset', tileset_size=Vec2(8,4), parent=scene)
    tilemap.canvas.texture = 'tilemap_test_level'
    camera.orthographic = True
    camera.position = tilemap.tilemap.size / 2
    camera.fov = tilemap.tilemap.height
    Text('press tab to toggle edit mode', position=window.top_left)
    app.run()
