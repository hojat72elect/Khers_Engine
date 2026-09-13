from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.editor.level_editor import *

if __name__ == '__main__':
    app = Ursina(vsync=False)

    class Tree(Entity):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.model = 'cube'
            self.color = color.brown
            self.top = Entity(name='tree_top', parent=self, y=1.5, model='cube', color=color.green, selectable=True)
            LEVEL_EDITOR.entities.append(self.top)

    level_editor = LevelEditor()
    level_editor.class_menu.available_classes |= {'WhiteCube': WhiteCube, 'EditorCamera':EditorCamera, 'FirstPersonController':FirstPersonController}
    app.run()
