from ursina import Entity, Audio
from copy import copy

def duplicate(entity, copy_children=True, *args, **kwargs): # use a for loop instead of duplicate() if you can.
    if entity.__class__ == Entity:
        e = entity.__class__(entity.add_to_scene_entities, *args, **kwargs)
    else:
        e = entity.__class__(*args, **kwargs)


    if hasattr(entity, 'model') and entity.model:
        e.model = copy(entity.model)


    for name in entity.attributes:
        if name == 'model':
            continue
        if name == 'collider' and entity.collider and entity.collider.name:
            # TODO: currently only copies colliders set with strings, not custom colliders.
            e.collider = entity.collider.name
            continue
        if name == 'scripts':
            for script in entity.scripts:
                e.add_script(copy(script))
            continue

        else:
            if hasattr(entity, name):
                setattr(e, name, getattr(entity, name))

    e.shader_input = entity.shader_input

    for c in entity.children:
        clone = duplicate(c, copy_children=False)
        clone.world_parent = e

    if isinstance(e, Audio):
        e.volume = entity.volume
        e.pitch = entity.pitch
        e.balance = entity.balance
        e.loop = entity.loop
        e.loops = entity.loops
        e.autoplay = entity.autoplay

        e.clip = entity.clip


    if hasattr(entity, 'text'):
        e.text = entity.text


    for key, value in kwargs.items():
        setattr(e, key ,value)

    return e
