from ursina import *

def combine(combine_parent, analyze=False, auto_destroy=True, ignore=[], ignore_disabled=True, include_normals=False):
    if not combine_parent.children:
        print_warning('Error, trying to combine children of entity with no children.', combine_parent.children)
        return

    verts = []
    tris = []
    norms = []
    uvs = []
    cols = []
    to_destroy = []
    o = 0
    original_texture = combine_parent.texture

    for e in scene.entities:
        if e in ignore:
            continue

        if ignore_disabled and not e.enabled:
            continue

        if e.has_ancestor(combine_parent) or e == combine_parent:
            if not hasattr(e, 'model') or e.model == None or e.scripts or e.eternal:
                continue
            if not hasattr(e.model, 'vertices') or not e.model.vertices:
                e.model = load_model(e.model.name, use_deepcopy=True)
                e.origin = e.origin
            if not e.model:
                continue

            if analyze:
                print('combining:', e)

            vertex_to_world_matrix = e.model.getTransform(combine_parent).getMat()
            world_space_verts = [Vec3(*vertex_to_world_matrix.xformPoint(Vec3(*v))) for v in e.model.vertices]
            verts += world_space_verts

            if not e.model.triangles:
                new_tris = [i for i in range(len(e.model.vertices))]

            else:
                new_tris = list()
                for t in e.model.triangles:
                    if isinstance(t, int):
                        new_tris.append(t)
                    elif len(t) == 3:
                        new_tris.extend(t)
                    elif len(t) == 4: # turn quad into tris
                        new_tris.extend([t[0], t[1], t[2], t[2], t[3], t[0]])

            new_tris = [t+o for t in new_tris]
            new_tris = [(new_tris[i], new_tris[i+1], new_tris[i+2]) for i in range(0, len(new_tris)-1, 3)]

            o += len(e.model.vertices)
            tris += new_tris

            if not auto_destroy: # need this data for static batching
                e.tris = new_tris
                e.world_space_verts = world_space_verts

            if e.model.uvs:
                uvs.extend([(uv * e.texture_scale) + e.texture_offset for uv in e.model.uvs])
            else:
                uvs.extend([(0,0) for e in e.model.vertices])

            if e.model.colors: # if has vertex colors
                cols.extend([Color(*vcol) * e.color for vcol in e.model.colors])
            else:
                cols.extend((e.color, ) * len(e.model.vertices))

            if include_normals:
                rotation_scale_matrix = vertex_to_world_matrix.getUpper3()  # get the rotation and scaling part of the matrix
                normal_to_world_matrix = rotation_scale_matrix
                normal_to_world_matrix.invertInPlace()
                normal_to_world_matrix.transposeInPlace()

                if e.model.normals: # if has normals
                    norms.extend([Vec3(*normal_to_world_matrix.xform(Vec3(*n)))for n in e.model.normals])
                else:
                    norms.extend((Vec3.up, ) * len(e.model.vertices))


            if auto_destroy and e != combine_parent:
                to_destroy.append(e)

    if auto_destroy:
        from ursina import destroy
        [destroy(e) for e in to_destroy]

    combine_parent.model = Mesh(vertices=verts, triangles=tris, normals=norms, uvs=uvs, colors=cols, mode='triangle')
    combine_parent.texture = original_texture
    # print('combined')
    # entity.model = Mesh(vertices=verts,  mode='triangle')
    # entity.flatten_strong()
    if analyze:
        render.analyze()
    return combine_parent.model
