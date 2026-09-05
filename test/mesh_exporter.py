from ursina import Ursina, Entity, load_model, EditorCamera, Sky
from ursina.mesh_exporter import ursinamesh_to_dae
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
