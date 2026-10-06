from ursina import Ursina, camera, color, shaders
from ursina.entity import Entity
from ursina.prefabs.editor_camera import EditorCamera

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True
    e = Entity()
    e.model = 'quad'
    e.color = color.random_color()
    e.position = (-2, 0, 10)
    e = Entity()
    e.model = 'quad'
    e.color = color.random_color()
    e.position = (2, 0, 10)
    e = Entity()
    e.model = 'quad'
    e.color = color.random_color()
    e.position = (0, 0, 40)
    EditorCamera()
    camera.shader = shaders.camera_grayscale_shader
    app.run()
