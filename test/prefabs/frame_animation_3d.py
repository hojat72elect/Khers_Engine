from ursina import Ursina, application, EditorCamera
from ursina.prefabs.frame_animation_3d import FrameAnimation3d

if __name__ == '__main__':
    application.asset_folder = application.asset_folder.parent.parent / 'samples'
    app = Ursina()
    '''
    Loads an obj sequence as a frame animation.
    So if you have some frames named run_cycle_000.obj, run_cycle_001.obj, run_cycle_002.obj and so on,
    you can load it like this: FrameAnimation3d('run_cycle_')
    '''
    FrameAnimation3d('blob_animation_')
    EditorCamera()
    app.run()
