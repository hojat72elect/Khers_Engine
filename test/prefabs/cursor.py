from ursina import Button, Mesh, Ursina, camera, Cursor, mouse

if __name__ == '__main__':
    app = Ursina()
    Button('button').fit_to_text()
    camera.orthographic = True
    camera.fov = 100
    cursor = Cursor(model=Mesh(vertices=[(-.5,0,0),(.5,0,0),(0,-.5,0),(0,.5,0)], triangles=[(0,1),(2,3)], mode='line', thickness=2), scale=0.02)
    mouse.visible = False
    app.run()
