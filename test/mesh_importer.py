from ursina import Ursina, EditorCamera, Sky, application, print_warning
from ursina.mesh_importer import compress_internal, obj_to_ursinamesh

if __name__ == '__main__':
    compress_internal()
    app = Ursina()
    m = obj_to_ursinamesh(folder=application.asset_folder.parent / 'samples', name='procedural_rock_0', save_to_file=False, delete_obj=False)

    if m is not None:
        print(m.serialize())
    else:
        print_warning("Failed to load procedural_rock_0.obj - file not found or parsing failed")

    EditorCamera()
    Sky(texture='sky_sunset')
    app.run()