from ursina import Ursina, Entity, camera, EditorCamera, ThinSlider
from ursina.shaders.screenspace_shaders.camera_contrast import camera_contrast_shader

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model='sphere')
    e = Entity(model='cube', y=-1)
    camera.shader = camera_contrast_shader
    camera.set_shader_input('contrast', 1)
    slider = ThinSlider(max=2, dynamic=True, position=(-.25, -.45))

    def adjust_contrast():
        camera.set_shader_input("contrast", slider.value)

    slider.on_value_changed = adjust_contrast
    EditorCamera()
    app.run()