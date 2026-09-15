from ursina.mesh import Mesh
from ursina.vec2 import Vec2
from ursina.vec3 import Vec3
from ursina.ursinastuff import Default

'''
nineslice mesh:

11-10--15--14
|   |   |   |
8---9--12--13
|   |   |   |
3---2---7---6
|   |   |   |
0---1---4---5

'''

class NineSlice(Mesh):
    outset = .4     # nineslice textures may have different padding due to baked drop shadows for example, so you can use this to account for that by making the model extend out.

    def __init__(self, entity_scale=Vec2.one, radius=.5, outset=Default):
        if isinstance(entity_scale, Vec3):
            entity_scale = entity_scale.xy
        elif isinstance(entity_scale, float | int):
            entity_scale = Vec2(entity_scale)
        elif isinstance(entity_scale, tuple | list):
            entity_scale = Vec2(*entity_scale)


        outset = __class__.outset if outset is Default else outset
        outset /= 1/radius  # account for different radius so you can change radius without having to change offset

        aspect_ratio = (entity_scale.x / entity_scale.y)
        verts = [Vec2(*e)*1 for e in (
            *((Vec2(-.5,-.5),) * 4),
            *((Vec2(.5,-.5),) * 4),
            *((Vec2(-.5,.5),) * 4),
            *((Vec2(.5,.5),) * 4),
            )]

        if entity_scale.x > entity_scale.y:
            aspect_ratio = (entity_scale.x / entity_scale.y)
            for idx in (1,2,9,10):
                verts[idx].x += radius / aspect_ratio
            for idx in (4,7,12,15):
                verts[idx].x -= radius / aspect_ratio
            for idx in (3,2,7,6):
                verts[idx].y += radius
            for idx in (8,9,12,13):
                verts[idx].y -= radius

            if outset:
                for idx in (0,3,8,11):
                    verts[idx].x -= outset / aspect_ratio
                for idx in (5,6,13,14):
                    verts[idx].x += outset / aspect_ratio
                for idx in (0,1,4,5):
                    verts[idx].y -= outset
                for idx in (11,10,15,14):
                    verts[idx].y += outset

        else:
            aspect_ratio = (entity_scale.y / entity_scale.x)
            for idx in (1,2,9,10):
                verts[idx].x += radius
            for idx in (4,7,12,15):
                verts[idx].x -= radius
            for idx in (3,2,7,6):
                verts[idx].y += radius / aspect_ratio
            for idx in (8,9,12,13):
                verts[idx].y -= radius / aspect_ratio

            if outset:
                for idx in (0,3,8,11):
                    verts[idx].x -= outset
                for idx in (5,6,13,14):
                    verts[idx].x += outset
                for idx in (0,1,4,5):
                    verts[idx].y -= outset / aspect_ratio
                for idx in (11,10,15,14):
                    verts[idx].y += outset / aspect_ratio

        super().__init__(
            vertices=[Vec3(*p,0) for p in verts],
            triangles=(
                (0,1,2,3),
                (1,4,7,2),
                (4,5,6,7),
                (3,2,9,8,),
                (2,7,12,9),
                (7,6,13,12),
                (8,9,10,11),
                (9,12,15,10),
                (12,13,14,15)
                ),
            uvs=(
                (0,0), (.5,0), (.5,.5), (0,.5),
                (.5,0), (1,0), (1,.5), (.5,.5),
                (0,.5), (.5,.5), (.5,1), (0,1),
                (.5,.5), (1,.5), (1,1), (.5,1)
                ),
            )
