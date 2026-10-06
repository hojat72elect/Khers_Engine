from ursina import EditorCamera, Ursina
from ursina.entity import Entity
from ursina.scripts.project_uvs import project_uvs

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model='sphere', texture='ursina_logo')
    project_uvs(e.model)
    EditorCamera()
    app.run()
