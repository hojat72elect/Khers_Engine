from ursina import Ursina, Entity, Text, Mesh, Vec3, color,copy, deepcopy, window, EditorCamera
from ursina.shaders.unlit_shader import unlit_shader

if __name__ == '__main__':
    app = Ursina()
    Entity.default_shader = unlit_shader

    # verts as list of tuples
    e = Entity(position=(0,0), model=Mesh(vertices=[(-0.5, 0, 0), (0.5, 0, 0), (0, 1, 0)]))

    # verts as tuple of tuples
    e = Entity(position=(1,0), model=Mesh(vertices=((-.5,0,0), (.5,0,0), (0, 1, 0))))
    Text(parent=e, text='triangle mesh\nwith verts as tuple of tuples', y=1, scale=5, origin=(0,-.5))

    # verts as list of lists
    e = Entity(position=(0,-2), model=Mesh(vertices=[[-.5,0,0], [.5,0,0], [0, 1, 0]]))
    Text(parent=e, text='triangle mesh\nwith verts as list of lists', y=1, scale=5, origin=(0,-.5))

    # verts as tuple of lists
    e = Entity(position=(1,-2), model=Mesh(vertices=([-.5,0,0], [.5,0,0], [0, 1, 0])))
    Text(parent=e, text='triangle mesh\nwith verts as tuple of lists', y=1, scale=5, origin=(0, -0.5))

    # verts as list Vec3
    e = Entity(position=(0,-4), model=Mesh(vertices=[Vec3(-.5,0,0), Vec3(.5,0,0), Vec3(0, 1, 0)]))
    Text(parent=e, text='triangle mesh\nwith verts as list Vec3', y=1, scale=5, origin=(0,-.5))

    # tris as flat list
    e = Entity(position=(1,-4), model=Mesh(
        vertices=[Vec3(-.5,0,0), Vec3(.5,0,0), Vec3(0, 1, 0)],
        triangles = [0,1,2],
    ))
    Text(parent=e, text='triangle mesh\nwith tris as flat list', y=1, scale=5, origin=(0,-.5))

    # tris as list of triangles
    e = Entity(position=(2.5,0), model=Mesh(
        vertices=[Vec3(-.5,0,0), Vec3(.5,0,0), Vec3(0, 1, 0)],
        triangles = [(0,1,2), (2,1,0)],  # should be double-sided
    ))
    Text(parent=e, text='triangle mesh\nwith tris as list of triangles', y=1, scale=5, origin=(0,-.5))

    continious_line = Entity(position=(4,0), model=Mesh(
        vertices=(Vec3(0,0,0), Vec3(.6,.3,0), Vec3(1,1,0), Vec3(.6,1.7,0), Vec3(0,2,0)),
        # triangles= ((0,1), (3,4,5)),
        mode='line',
        thickness=4,
        ), color=color.cyan)
    Text(parent=continious_line, text='continious_line', y=1, scale=5)

    line_segments = Entity(position=(4,-2), model=Mesh(
        vertices=(Vec3(0,0,0), Vec3(.6,.3,0), Vec3(1,1,0), Vec3(.6,1.7,0), Vec3(0,2,0)),
        triangles= ((0,1), (3,4)),
        mode='line',
        thickness=4,
        ), color=color.magenta)
    Text(parent=line_segments, text='line_segments', y=1, scale=5)

    points_3d = Entity(position=(6,0), model=Mesh(vertices=(Vec3(0,0,0), Vec3(.6,.3,0), Vec3(1,1,0), Vec3(.6,1.7,0), Vec3(0,2,0)), mode='point', thickness=.05), color=color.red, texture='circle')
    Text(parent=points_3d, text='points_3d', y=1, scale=5)

    points_2d = Entity(position=(6,-2), model=Mesh(vertices=(Vec3(0,0,0), Vec3(.6,.3,0), Vec3(1,1,0), Vec3(.6,1.7,0), Vec3(0,2,0)), mode='point', thickness=10, render_points_in_3d=False), color=color.red, texture='circle')
    Text(parent=points_2d, text='points_2d', y=1, scale=5)
    points_2d.set_shader_auto()
    print('----------------------', points_2d.model.getShader())

    quad = Entity(
        position=(8,0),
        model=Mesh(
            vertices=((0.5, 0.5, 0.0), (-0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (0.5, 0.5, 0.0), (-0.5, -0.5, 0.0)),
            uvs=((1, 1), (0, 1), (0, 0), (1, 0), (1, 1), (0, 0)),
            mode='triangle'),
        texture='shore'
        )
    Text(parent=quad, text='quad_with_uvs', y=1, scale=5, origin=(0,-.5))

    quad = Entity(
        position=(8,-2),
        model=Mesh(
            vertices=((0.5, 0.5, 0.0), (-0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (0.5, 0.5, 0.0), (-0.5, -0.5, 0.0)),
            uvs=((1, 1), (0, 1), (0, 0), (1, 0), (1, 1), (0, 0)),
            normals=[(-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0)],
            mode='triangle'),
        )
    Text(parent=quad, text='quad_with_normals', y=1, scale=5, origin=(0,-.5))

    quad = Entity(
        position=(8,-4),
        model=Mesh(
            vertices=((0.5, 0.5, 0.0), (-0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (0.5, 0.5, 0.0), (-0.5, -0.5, 0.0)),
            uvs=((1, 1), (0, 1), (0, 0), (1, 0), (1, 1), (0, 0)),
            normals=[(-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0)],
            mode='triangle'),
        texture='shore',
        )
    Text(parent=quad, text='quad_with_usv_and_normals', y=1, scale=5, origin=(0,-.5))

    quad = Entity(
        position=(8,-6),
        model=Mesh(
            vertices=((0.5, 0.5, 0.0), (-0.5, 0.5, 0.0), (-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (0.5, 0.5, 0.0), (-0.5, -0.5, 0.0)),
            uvs=((1, 1), (0, 1), (0, 0), (1, 0), (1, 1), (0, 0)),
            normals=[(-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0), (-0.0, 0.0, -1.0)],
            colors=[color.red, color.yellow, color.green, color.cyan, color.blue, color.magenta],
            mode='triangle'),
        texture='shore'
        )
    Text(parent=quad, text='quad_with_usv_and_normals_and_vertex_colors', y=1, scale=5, origin=(0,-.5))

    quad = Entity(
        position=(10,0),
        model=Mesh(
            vertices=((-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (0.5, 0.5, 0.0), (-0.5, 0.5, 0.0)),
            triangles=(0,1,2, 2,3,0),
            mode='triangle'),
        )
    Text(parent=quad, text='triangles flat', y=1, scale=5, origin=(0,-.5))

    quad = Entity(
        position=(10,-2),
        model=Mesh(
            vertices=((-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (0.5, 0.5, 0.0), (-0.5, 0.5, 0.0)),
            triangles=((0,1,2), (2,3,0)),
            mode='triangle'),
        )
    Text(parent=quad, text='triangles triplets', y=1, scale=5, origin=(0,-.5))

    quad = Entity(
        position=(10,-4),
        model=Mesh(
            vertices=((-0.5, -0.5, 0.0), (0.5, -0.5, 0.0), (0.5, 0.5, 0.0), (-0.5, 0.5, 0.0)),
            triangles=((0,1,2,3), (0,3,2)),
            mode='triangle'),
        )
    Text(parent=quad, text='triangles quad + tri', y=1, scale=5, origin=(0,-.5))

    copy_test = Entity(position=(12,0), model=copy(quad.model))
    Text(parent=copy_test, text='copy_test', y=1, scale=5, origin=(0,-.5))

    deepcopy_test = Entity(position=(12,-2), model=deepcopy(quad.model))
    Text(parent=deepcopy_test, text='deepcopy_test', y=1, scale=5, origin=(0,-.5))

    clear_test = Entity(position=(12,-4), model=deepcopy(quad.model))
    clear_test.model.clear()
    Text(parent=clear_test, text='.clear() test', y=1, scale=5, origin=(0,-.5))

    window.color = color.black
    EditorCamera()
    app.run()
