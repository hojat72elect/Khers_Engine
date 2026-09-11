from ursina import Ursina, Text, scene, EditorCamera, Vec2
from ursina.shaders.text_with_shadows_shader import text_with_shadows_shader

if __name__ == "__main__":
    app = Ursina()
    textEntity = Text("some <orange>COOL <default> text here", parent=scene, scale=25, shader=text_with_shadows_shader)

    def input(key):
        if key == "f":
            textEntity.fade_out()
        if key == "o":
            textEntity.set_shader_input("shadow_offset", Vec2(0.1, 0.1))

    EditorCamera()
    app.run()
