from ursina import Ursina
from ursina.editor.level_editor import LevelEditor
from ursina.editor.prefabs.sliced_cube import SlicedCube

if __name__ == '__main__':
    app = Ursina(borderless=False)
    level_editor = LevelEditor()
    level_editor.goto_scene(0,0)
    sliced_cube = SlicedCube(selectable=True, texture='sliceable_cube_template', shader='unlit_shader', scale_multiplier=1.5)

    def input(key):
        if key == 'space':
            sliced_cube.generate()

    level_editor.add_entity(sliced_cube)
    app.run()