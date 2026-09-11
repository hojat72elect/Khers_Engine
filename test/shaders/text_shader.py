from ursina import Ursina, Text, EditorCamera, scene
from ursina.shaders.text_shader import text_shader

if __name__ == "__main__":
    app = Ursina()
    textEntity = Text("some <orange>COOL <default> text here", parent=scene, scale=25)
    text_shader.compile()

    for textNode in textEntity.text_nodes:
        textNode.setShader(text_shader._shader)
        for key, value in text_shader.default_input.items():
            textNode.setShaderInput(key, value)
            print(textNode.getColorScale())

    EditorCamera()
    app.run()
