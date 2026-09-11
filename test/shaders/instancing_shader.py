import random
from ursina import (
    Cone,
    EditorCamera,
    Entity,
    Quat,
    Ursina,
    Vec3,
    application,
    color,
    window,
)
from ursina.shaders.instancing_shader import instancing_shader

if __name__ == "__main__":
    window.vsync = False
    app = Ursina()

    instances = []
    Entity(model="plane", texture="grass", scale=128)
    application.asset_folder = application.asset_folder.parent.parent
    p = Entity(model=Cone(5), y=1, texture="brick")
    p.model.uvs = [(v[0], v[1]) for v in p.model.vertices]
    p.model.generate()
    p.shader = instancing_shader
    p.setInstanceCount(256)

    for z in range(16):
        for x in range(16):
            e = Entity(add_to_scene_entities=False, position=Vec3(x, 0, z), color=color.lime, rotation_y=random.random() * 360)
            instances.append(e)
            print(e.quaternion, Quat())

    p.set_shader_input("position_offsets", [e.position * 4 for e in instances])
    p.set_shader_input("rotation_offsets", [e.quaternion for e in instances])
    p.set_shader_input("scale_multipliers", [e.scale * random.uniform(0.9, 2) for e in instances])
    print(len(p.model.vertices) * len(instances))
    EditorCamera()
    app.run()
