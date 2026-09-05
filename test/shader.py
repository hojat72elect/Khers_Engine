from ursina import Ursina, Entity, held_keys, scene, EditorCamera, Shader
from time import perf_counter
from ursina.shaders.unlit_shader import unlit_shader
from ursina.shaders.matcap_shader import matcap_shader

if __name__ == '__main__':
   
    t = perf_counter()
    app = Ursina()
    Entity(model='cube', shader=Shader(name='test_shader'))
    EditorCamera()

    def input(key):
        if held_keys['control'] and key == 'r':
            reload_shaders()

    def reload_shaders():
        for e in scene.entities:
            if hasattr(e, '_shader'):
                print('-------', e.shader)

    combined_shader = unlit_shader + matcap_shader
    print(combined_shader)
    app.run()
