from ursina import Ursina
from ursina.prefabs.editor_camera import EditorCamera
from ursina.prefabs.sky import Sky
from ursina.entity import Entity
from ursina.mesh_exporter import ursinamesh_to_dae
from ursina.mesh_importer import load_model
from time import perf_counter

if __name__ == '__main__':
    app = Ursina()
    t = perf_counter()
    Entity(model='untitled')
    print('-------', perf_counter() - t)
    m = load_model('cube', use_deepcopy=True)
    ursinamesh_to_dae(m, 'dae_export_test')
    EditorCamera()
    Sky(texture='sky_sunset')
    app.run()
