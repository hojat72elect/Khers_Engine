from ursina import Ursina, Entity, load_model, application, Sky, color, EditorCamera
import random

if __name__ == '__main__':
    app = Ursina()
    for i in range(10):
        e = Entity(model=load_model('sphere', path=application.internal_models_compressed_folder, use_deepcopy=True))
        e.position = (random.uniform(-3,3),random.uniform(-3,3),random.uniform(-3,3))
        e.rotation = (random.uniform(0,360),random.uniform(0,360),random.uniform(0,360))
        e.scale = random.uniform(1,3)
        e.model.colorize(smooth=False, world_space=True, strength=.5)

    Sky(color=color.gray)
    EditorCamera()
    app.run()
