import sys
from ursina import application
from ursina.scene import instance as scene
from ursina.ursinastuff import invoke
from ursina.sequence import Sequence

def destroy(entity, delay=0, unscaled=True, ignore_paused=False, force_destroy=False):
    if application.development_mode:
        # get the calling function and the file it's from, so we can give a better error message if we try to use it after destroy
        entity.destroy_source = f'caller: {sys._getframe(1).f_code.co_name} file: {sys._getframe(1).f_code.co_filename}'

    if delay == 0:
        _destroy(entity, force_destroy=force_destroy)
        return True

    return invoke(_destroy, entity, delay=delay, unscaled=unscaled, ignore_paused=ignore_paused, force_destroy=force_destroy)
    # return Sequence(Wait(delay), Func(_destroy, entity), auto_destroy=True, started=True)

def _destroy(entity, force_destroy=False):
    # from ursina import camera
    # if not entity or entity == camera:
    #     return

    if entity.eternal and not force_destroy:
        return

    if hasattr(entity, 'scripts'):
        for s in entity.scripts:
            del s

    if hasattr(entity, 'animations'):
        for anim in entity.animations:
            if anim:
                anim.kill()

    for child in entity.children:
        _destroy(child)

    if entity.collider and hasattr(entity.collider, 'remove'):
        entity.collider.remove()

    if hasattr(entity, 'clip') and hasattr(entity, 'stop'): # stop audio
        entity.stop(False)

    if hasattr(entity, 'on_destroy'):
        entity.on_destroy()

    if entity in scene.entities:
        scene._entities_marked_for_removal.append(entity)

    if entity in scene.collidables:
        scene.collidables.remove(entity)

    if hasattr(entity, '_parent') and entity._parent and hasattr(entity._parent, '_children') and entity in entity._parent._children:
        entity._parent._children.remove(entity)

    for e in entity.loose_children:
        destroy(e)

    if hasattr(entity, '_loose_parent') and entity._loose_parent and hasattr(entity._loose_parent, '_loose_children') and entity in entity._loose_parent._loose_children:
        entity._loose_parent._loose_children.remove(entity)

    if hasattr(entity, 'tooltip'):
        _destroy(entity.tooltip)

    if hasattr(entity, '_on_click') and isinstance(entity._on_click, Sequence):
        entity._on_click.kill()

    if entity.hasPythonTag("Entity"):
        entity.clearPythonTag("Entity")

    entity.removeNode()

    # if hasattr(entity.__class__, 'instances') and entity in entity.__class__.instances:
    #     entity.__class__.instances.remove(entity)
    #unload texture
    # if hasattr(entity, 'texture') and entity.texture != None:
    #     entity.texture.releaseAll()

    # del entity
