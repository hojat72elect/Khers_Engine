from ursina import Ursina, Entity, color, Text, window, EditorCamera, Vec3, Vec2
from ursina.shaders.lit_with_shadows_shader import lit_with_shadows_shader

if __name__ == '__main__':
    app = Ursina()
    Entity.default_shader = lit_with_shadows_shader
    combine_parent = Entity(texture='brick')
    e1 = Entity(parent=combine_parent, model='sphere', y=1.5, color=color.pink, rotation_y=90)
    e2 = Entity(parent=combine_parent, model='cube', color=color.yellow, x=1, origin_y=-.5, texture='brick')
    e3 = Entity(parent=e2, model='cube', color=color.yellow, y=2, scale=.5, texture='brick', texture_scale=Vec2(3,3), texture_offset=(.1,.1))
    e4 = Entity(parent=combine_parent, model='plane', color=color.lime, scale=10, texture='brick', texture_scale=Vec2(5,5))
    Text(position=window.top, origin=(0,.5), text='Press space to combine')

    def input(key):
        if key == 'space':
            from time import perf_counter
            t = perf_counter()
            combine_parent.combine(include_normals=True)
            combine_parent.shader = lit_with_shadows_shader
            print('combined in:', perf_counter() - t)

    from ursina.lights import DirectionalLight
    sun = DirectionalLight()
    sun.look_at(Vec3(-1,-1,-1))
    EditorCamera()
    app.run()
