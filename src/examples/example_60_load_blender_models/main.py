from ursina import Ursina, Entity, EditorCamera

app = Ursina(borderless=False)
Entity(model='blender_test_model', collider='mesh')
EditorCamera()
app.run()
