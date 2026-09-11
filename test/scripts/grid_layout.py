from ursina import Ursina, Entity, color, Button, camera, time, EditorCamera, grid_layout, window, Vec2, Tooltip, Circle, Func

if __name__ == '__main__':
    app = Ursina()
    center = Entity(model='quad', scale=.025, color=color.red, always_on_top=True)
    p = Entity()
    
    for i in range(13):
        b = Button(parent=p, model='quad', scale=Vec2(.2,.1), text=str(i), color=color.tint(color.random_color(), -0.6))
        b.text_entity.scale = 1
        
    t = time.time()
    grid_layout(p.children, origin=(0,.5), spacing=(.1,.1))
    center = Entity(parent=camera.ui, model=Circle(), scale=.005, color=color.lime)
    EditorCamera()
    print(time.time() - t)

    # test
    for e in [(-.5,.5), (0,.5), (.5,.5), (-.5,0), (0,0), (.5,0), (-.5,-.5), (0,-.5), (.5,-.5)]:
        Button(
            text="*",
            model="quad",
            text_origin=e,
            scale=0.095,
            origin=(-0.5, 0.5),
            position=window.top_left + Vec2(*e) * 0.2 + Vec2(0.1, -0.1),
            tooltip=Tooltip(str(e)),
            on_click=Func(grid_layout, p.children, max_x=4, origin=e, spacing=(0.05, 0.05))
        )

    app.run()