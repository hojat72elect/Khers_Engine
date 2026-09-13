from ursina import Ursina
from ursina.editor.level_editor import LevelEditor
from ursina.editor.prefabs.pipe_editor import PipeEditor

if __name__ == '__main__':
    app = Ursina(borderless=False)
    level_editor = LevelEditor()
    level_editor.goto_scene(0,0)
    level_editor.entities.append(PipeEditor())
    app.run()
