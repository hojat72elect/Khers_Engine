from ursina import Ursina, Entity, color, Pipe, Circle, EditorCamera

if __name__ == '__main__':
    app = Ursina()
    path = [e*5 for e in Circle().vertices]
    path.append(path[0])
    thicknesses = ((1,1), (.5,.5), (.75,.75), (.5,.5), (1,1))
    e = Entity(model=Pipe(path=path, cap_ends=False, thicknesses=thicknesses), texture='shore')
    color_gradient = [color.magenta, color.cyan.tint(-.5), color.clear]
    color_gradient = color_gradient[::-1]
    print(len(e.model.vertices), len(e.model.colors))
    EditorCamera()
    origin = Entity(model='cube', color=color.magenta)
    origin.scale *= .25
    app.run()
