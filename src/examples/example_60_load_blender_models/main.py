from ursina.prefabs.editor_camera import EditorCamera
from ursina.main import Ursina
from ursina.entity import Entity

app = Ursina(borderless=False)
Entity(model='blender_test_model', collider='mesh')
EditorCamera()
app.run()
