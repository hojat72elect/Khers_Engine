from ursina import Ursina, Entity, color, EditorCamera, destroy, Cone

if __name__ == '__main__':
    app = Ursina()
    graphics = Entity(model=Cone(8, radius=.4, height=2), origin_y=-.5, color=color.hex('#121024'))
    Entity(model='wireframe_cube')
    origin = Entity(model='quad', color=color.orange, scale=(.05, .05))
    ed = EditorCamera()
    
    def input(key):
        global graphics
        if key == 'd':
            destroy(graphics)
            graphics.model = None
        if key == 'space':
            graphics = Entity(model=Cone(8, radius=.4, height=2), origin_y=-.5, color=color.hex('#121024'))

    app.run()

