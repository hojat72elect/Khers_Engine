from ursina import Ursina, color, camera, scene, EditorCamera, Grid, NineSlice
from ursina.entity import Entity
from ursina.vec2 import Vec2
from ursina.vec3 import Vec3
from ursina.prefabs.draggable import Draggable
from ursina.prefabs.button import Button

if __name__ == '__main__':
    app = Ursina()
    Button.default_texture = 'nineslice_rainbow'
    Button.default_color = color.white
    m = NineSlice(entity_scale=Vec3(2,1,1))
    Entity(parent=camera.ui, model='wireframe_quad', scale=Vec2(2,1)*.1, color=color.red)
    NineSlice.outset = .4
    button_1 = Draggable(parent=scene, radius=.5, model=NineSlice, scale=1, position=(0,0), origin=(-.5,-.5), texture="nineslice_rainbow", color=color.white) # if entity_scale is not provided to NineSlice, use self.scale
    button_2 = Draggable(parent=scene, radius=.5, model=NineSlice((2,1)), scale=(2,1), position=(0,1), origin=(-.5,-.5), texture="nineslice_rainbow", color=color.white, wireframe=1)
    button_2.texture = None
    button_3 = Draggable(parent=scene, radius=.5, model=NineSlice, scale=(1,3), position=(1,-2), origin=(-.5,-.5))
    button_4 = Draggable(parent=scene, radius=.25, model=NineSlice, scale=(3,1), position=(-2,-1), origin=(-.5,-.5))
    EditorCamera()
    Entity(model=Grid(8,8), scale=8)
    app.run()