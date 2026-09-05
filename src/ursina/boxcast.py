from ursina import color
from ursina.entity import Entity
from ursina.scene import instance as scene
from ursina.ursinastuff import invoke
from ursina.vec3 import Vec3

_boxcast_box = Entity(model='cube', origin_z=-.5, collider='box', color=color.white33, enabled=False, eternal=True, add_to_scene_entities=False)

def boxcast(origin, direction=(0,0,1), distance=9999, thickness=(1,1), traverse_target=scene, ignore:list=None, debug=False): # similar to raycast, but with width and height
    if not ignore:
        ignore = []

    if isinstance(thickness, int | float | complex):
        thickness = (thickness, thickness)

    _boxcast_box.enabled = True
    _boxcast_box.collision = True
    _boxcast_box.position = origin
    _boxcast_box.scale = Vec3(abs(thickness[0]), abs(thickness[1]), abs(distance))
    _boxcast_box.always_on_top = debug
    _boxcast_box.visible = debug

    _boxcast_box.look_at(origin + direction)
    hit_info = _boxcast_box.intersects(traverse_target=traverse_target, ignore=ignore)

    if debug:
        _boxcast_box.collision = False
        invoke(setattr, _boxcast_box, 'enabled', False, delay=.2)
    else:
        _boxcast_box.enabled = False

    return hit_info
