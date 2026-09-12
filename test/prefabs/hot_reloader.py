from ursina import Ursina, EditorCamera, Sky, color, held_keys, time
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.primitives import AzureCube, WhiteSphere, GrayPlane
from ursina.lights import DirectionalLight

if __name__ == '__main__':
    """
    By default you can press F5 to reload the starting script, F6 to reimport textures and F7 to reload models.
    """
    app = Ursina()
    shader = lit_with_shadows_shader
    a = AzureCube(shader=shader, texture="shore")
    b = WhiteSphere(shader=shader, rotation_y=180, x=3, texture="brick")
    b.texture.filtering = None
    GrayPlane(scale=10, y=-2, texture="shore", shader=shader)

    # Enable shadows. we need to set a frustum for that.
    sun = DirectionalLight(y=10, rotation=(90+30,90,0))
    sun._light.show_frustum()
    Sky(color=color.light_gray)
    print(Sky.instances)
    EditorCamera()

    def update():
        a.x += (held_keys['d'] - held_keys['a']) * time.dt * 5
        a.y += (held_keys['e'] - held_keys['q']) * time.dt * 5
        a.z += (held_keys['w'] - held_keys['s']) * time.dt * 5

    app.run()