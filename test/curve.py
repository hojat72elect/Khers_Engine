from ursina import Entity, Mesh, Text, Ursina, camera, color, curve, window, floor, EditorCamera, Vec3
from ursina.curve import CubicBezier,combine, linear, reverse, in_expo

if __name__ == '__main__':
    '''Draws a sheet with every curve and its name'''
    
    app = Ursina()
    camera.orthographic = True
    camera.fov = 16
    camera.position = (9, 6)
    window.color = color.black

    def render_curve(curve_function, name):
        curve_renderer = Entity(model=Mesh(vertices=[Vec3(i / 31, curve_function(i / 31), 0) for i in range(32)], mode='line', thickness=2), color=color.light_gray)
        _label = Text(parent=curve_renderer, text=name, scale=8, color=color.gray, y=-.1)
        return curve_renderer

    j = 0
    for e in dir(curve):
        try:
            item = getattr(curve, e)
            print(item.__name__, ":", item(0.75))
            curve_renderer = render_curve(item, item.__name__)
            row = floor(j / 8)
            curve_renderer.x = (j % 8) * 2.5
            curve_renderer.y = row * 1.75
            label = Text(parent=curve_renderer, text=item.__name__, scale=8, color=color.gray, y=-0.1)
            j += 1
        except:
            pass

    c = CubicBezier(0, .5, 1, .5)
    print('-----------', c.calculate(.23))
    window.exit_button.visible = False
    window.fps_counter.enabled = False
    custom_curve = combine(linear, reverse(in_expo), .25)
    render_curve(custom_curve, 'custom_curve')
    EditorCamera()
    app.run()
    
    '''
    These are used by Entity when animating, like this:

    e = Entity()
    e.animate_y(1, curve=curve.in_expo)

    e2 = Entity(x=1.5)
    e2.animate_y(1, curve=curve.CubicBezier(0,.7,1,.3))
    '''
