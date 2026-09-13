from ursina import EditorCamera, Entity, Ursina, load_texture, Vec3
from ursina.shaders.vertex_animation_shader import vertex_animation_shader

if __name__ == '__main__':
    app = Ursina()
    entity = Entity(model='cube', shader=vertex_animation_shader, texture='grass')
    animation_texture = load_texture('grass')
    entity.set_shader_input('total_frames', animation_texture.height)
    entity.set_shader_input('num_verts', animation_texture.width)
    entity.set_shader_input('frame_texture', animation_texture)
    entity.set_shader_input('pos_min', Vec3(-.5, -.5, -.5))
    entity.set_shader_input('pos_max', Vec3(.5, .5, .5))
    EditorCamera()
    entity.animate_shader_input('frame_index', 10, duration=3, loop=True)
    app.run()