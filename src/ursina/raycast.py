import builtins
from ursina.entity import Entity
from ursina.mesh import Mesh
from ursina.scene import instance as scene
from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay
from ursina.vec3 import Vec3
from copy import copy
from ursina.hit_info import HitInfo
from ursina import ursinamath, color
from ursina.destroy import destroy

_line_model = Mesh(vertices=[Vec3(0,0,0), Vec3(0,0,1)], mode='line')
_raycaster = Entity(add_to_scene_entities=False)
_raycaster._picker = CollisionTraverser()  # Make a traverser
_raycaster._pq = CollisionHandlerQueue()  # Make a handler
_raycaster._pickerNode = CollisionNode('_raycaster')
_raycaster._pickerNode.set_into_collide_mask(0)
_raycaster._pickerNP = _raycaster.attach_new_node(_raycaster._pickerNode)
_raycaster._picker.addCollider(_raycaster._pickerNP, _raycaster._pq)
_ray = CollisionRay()
_ray.setOrigin(Vec3(0,0,0))
_ray.setDirection(Vec3(0,0,1))
_raycaster._pickerNode.addSolid(_ray)

def raycast(origin, direction:Vec3=(0,0,1), distance=9999, traverse_target:Entity=scene, ignore:list=None, debug=False, color=color.white):
    if not ignore:
        ignore = []

    _raycaster.position = origin
    _raycaster.look_at(_raycaster.position + direction)

    if debug:
        temp = Entity(position=origin, model=copy(_line_model), scale=Vec3(1,1,min(distance,9999)), color=color, add_to_scene_entities=False)
        temp.look_at(_raycaster.position + direction)
        destroy(temp, 1/30)

    _raycaster._picker.traverse(traverse_target)      #HALF!

    if _raycaster._pq.get_num_entries() == 0:
        _raycaster.hit = HitInfo(hit=False, distance=distance)
        return _raycaster.hit


    _raycaster._pq.sort_entries()
    entries = _raycaster._pq.getEntries()
    entities = [e.get_into_node_path().parent for e in entries]

    entries = [        # filter out ignored entities
        e for i, e in enumerate(entries)
        if entities[i] in scene.collidables
        and entities[i] not in ignore
        and ursinamath.distance(_raycaster.world_position, e.get_surface_point(builtins.render)) <= distance
        ]

    if len(entries) == 0:
        return HitInfo(hit=False)

    _raycaster.collision = entries[0]
    nP = _raycaster.collision.get_into_node_path().parent
    point = Vec3(*_raycaster.collision.get_surface_point(nP))
    world_point = Vec3(*_raycaster.collision.get_surface_point(builtins.render))

    hit_info = HitInfo(hit=True)
    hit_info.entities = [e.get_into_node_path().parent.getPythonTag('Entity') for e in entries]
    hit_info.entity = hit_info.entities[0]

    hit_info.point = point
    hit_info.world_point = world_point
    hit_info.distance = ursinamath.distance(_raycaster.world_position, hit_info.world_point)

    hit_info.normal = Vec3(*_raycaster.collision.get_surface_normal(_raycaster.collision.get_into_node_path().parent).normalized())
    hit_info.world_normal = Vec3(*_raycaster.collision.get_surface_normal(builtins.render).normalized())

    return hit_info
