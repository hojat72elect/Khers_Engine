from ursina import Ursina, Entity, EditorCamera, Mesh
from ursina.scripts.merge_vertices import merge_overlapping_vertices

if __name__ == '__main__':
    vertices = ((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 0, 0), (1, 1, 0), (0, 1, 0))
    tris = (0,1,2,3,4,5)
    newVertices, newTris = merge_overlapping_vertices(vertices, tris)
    print("verts:", vertices, newVertices)
    print('tris:', tris, newTris)
    app = Ursina()
    e = Entity(model=Mesh(newVertices, newTris, mode="triangle"))
    EditorCamera()

    app.run()