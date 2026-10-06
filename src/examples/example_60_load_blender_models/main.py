from ursina import Ursina, EditorCamera
from ursina.entity import Entity

app = Ursina(borderless=False)
Entity(model='blender_test_model', collider='mesh')
EditorCamera()
app.run()
