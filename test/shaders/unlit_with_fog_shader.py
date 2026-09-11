from ursina import EditorCamera, Entity, Ursina, color, Vec2
from ursina.shaders.unlit_with_fog_shader import unlit_with_fog_shader

if __name__ == '__main__':
    app = Ursina()
    shader = unlit_with_fog_shader
    a = Entity(model='cube', shader=shader)
    ground = Entity(model='plane', color=color.gray, scale=10, y=-2, texture='shore', shader=shader, texture_scale=(10,10))
    ground.set_shader_input('texture_scale', Vec2(2, 1))
    EditorCamera()
    app.run()
