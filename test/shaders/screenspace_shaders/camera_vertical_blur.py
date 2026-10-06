from ursina import Ursina, camera, window, color, mouse
from ursina.entity import Entity
from ursina.prefabs.slider import ThinSlider
from ursina.prefabs.editor_camera import EditorCamera
from ursina.shaders.screenspace_shaders.camera_vertical_blur import camera_vertical_blur_shader

if __name__ == '__main__':
    app = Ursina()
    window.color = color._16
    e = Entity(model='sphere', color=color.orange)
    e = Entity(model='cube', y=-1)
    camera.shader = camera_vertical_blur_shader
    slider = ThinSlider(max=.1, dynamic=True, position=(-0.25, -0.45))

    def set_blur():
        print(slider.value)
        camera.set_shader_input("blur_size", slider.value)

    def update():
        camera.set_shader_input('blur_size', mouse.x)

    slider.on_value_changed = set_blur
    EditorCamera()
    app.run()
