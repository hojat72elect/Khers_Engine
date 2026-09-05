from ursina import EditorCamera, Ursina, Vec3, color, Entity, DirectionalLight, Sky, shaders

if __name__ == '__main__':
    app = Ursina()

    Entity.default_shader = shaders.lit_with_shadows_shader # you have to apply this shader to entities for them to receive shadows.
    ground = Entity(model='plane', scale=10, texture='grass')
    lit_cube = Entity(model='cube', y=1, color=color.light_gray)

    light = DirectionalLight()
    light.look_at(Vec3(1,-1,1))

    dont_cast_shadow = Entity(model='cube', y=1, x=2, color=color.light_gray)
    dont_cast_shadow.hide(0b0001)

    unlit_entity = Entity(model='cube', y=1,x=-2, unlit=True, color=color.light_gray)
    bar = Entity(model='cube', position=(0,3,-2), scale=(10,.2,.2), color=color.light_gray)

    # How to render shows in a limited area.
    # to make it easier to see, make a box to define where we will have shadows. we can make this invisible after.
    shadow_bounds_box = Entity(model='wireframe_cube', scale=5, visible=0)
    light.update_bounds(shadow_bounds_box)
    EditorCamera(rotation=(30,30,0))
    Sky()
    app.run()
