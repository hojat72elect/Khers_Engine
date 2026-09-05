from ursina import EditorCamera, Entity, Ursina, camera, color, shaders

if __name__ == '__main__':
    app = Ursina()
    camera.orthographic = True

    e = Entity()
    e.model = 'quad'
    e.color = color.random_color()
    e.position = (-2, 0, 10)

    e = Entity()
    e.model = 'quad'
    e.color = color.random_color()
    e.position = (2, 0, 10)

    e = Entity()
    e.model = 'quad'
    e.color = color.random_color()
    e.position = (0, 0, 40)

    EditorCamera()
    camera.shader = shaders.camera_grayscale_shader
    app.run()
