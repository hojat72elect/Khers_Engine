from ursina import Ursina, Entity, camera, color, time, EditorCamera
from ursina.shaders.screenspace_shaders.camera_outline_shader import empty_shader

if __name__ == '__main__':
    app = Ursina()
    Entity(model='cube', texture='white_cube', color=color.red)
    Entity(model='cube', texture='white_cube', color=color.white, x=1.1)
    Entity(model='sphere', texture='white_cube', color=color.gray, y=1.1)
    camera.shader = empty_shader
    print(camera.shader)
    t = 0
    frame = 0

    def update():
      global t, frame
      t += time.dt
      frame += 1

    EditorCamera()
    app.run()
