from ursina import Ursina, Button, scene, EditorCamera, Entity, duplicate, color, Vec2, shaders

if __name__ == '__main__':
    app = Ursina()
    new_parent = Entity(scale=1)

    e = Button(parent=scene, scale=2, text='test', texture='shore', texture_scale=Vec2(2), color=color.gray)
    e.c = Entity(parent=e, model='icosphere', scale=.5, y=.5, shader=shaders.matcap_shader, texture='matcap_4')
    e.c2 = Entity(parent=e.c, model='cube', scale=.5, y=.5, x=1, color=color.green, shader=shaders.triplanar_shader, texture='grass')

    e2 = duplicate(e, x=2.25, parent=new_parent)
    EditorCamera()
    app.run()
