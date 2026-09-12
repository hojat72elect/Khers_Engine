from ursina import Ursina, Entity, Draggable, EditorCamera, scene, Func, color

if __name__ == '__main__':
    app = Ursina()
    Entity(model='plane', scale=8, texture='white_cube', texture_scale=(8,8))
    draggable_button = Draggable(scale=.1, text='drag me', position=(-.5, 0))
    world_space_draggable = Draggable(parent=scene, model='cube', color=color.azure, plane_direction=(0,1,0), lock=(1,0,0))
    EditorCamera(rotation=(30,10,0))
    world_space_draggable.drop = Func(print, 'dropped cube')
    app.run()
