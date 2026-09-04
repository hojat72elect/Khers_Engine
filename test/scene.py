from ursina import Ursina, EditorCamera, Entity, Sky, color, scene, camera
from ursina.shaders.unlit_with_fog_shader import unlit_with_fog_shader

if __name__ == "__main__":
    app = Ursina()
    Entity(model="plane", color=color.black, scale=100)
    EditorCamera()
    s = Sky()

    def input(key):
        if key == "l":
            for e in scene.entities:
                print(e.name)
        if key == "d":
            scene.clear()
            Entity(model="cube")

    Entity(model="cube", shader=unlit_with_fog_shader)
    unlit_with_fog_shader.fog_color = color.blue
    unlit_with_fog_shader.fog_density = (0, 100)
    Entity(parent=camera.ui, model="quad", scale=0.1)
    app.run()
