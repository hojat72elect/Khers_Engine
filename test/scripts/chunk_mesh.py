from ursina import EditorCamera, Entity, Grid, Mesh, Terrain, Ursina, Vec2, Vec3, color, flatten_list, enumerate_2d
from ursina.scripts.chunk_mesh import chunk_mesh

if __name__ == "__main__":
    app = Ursina()
    reference = Entity(x=-1, model=Terrain("heightmap_1", skip=4), texture="grass", texture_scale=(3, 3), origin=(-0.5, 0, -0.5), wireframe=True, color=color.green)
    target_mesh = reference.model
    target_mesh.vertices = [v + Vec3(0.5, 0, 0.5) for v in target_mesh.vertices]
    chunk_size = 1 / 8
    num_chunks = Vec2(8, 8)
    chunks = chunk_mesh(target_mesh, num_chunks, chunk_size)
    grid = Entity(x=-1, model=Grid(*num_chunks), rotation_x=90, color=color.red, scale=num_chunks * chunk_size, origin=(-0.5, -0.5))

    for (x, z), value in enumerate_2d(chunks):
        if not value:
            chunks[x][z] = Entity(model="cube", color=color.random_color(), position=Vec3(x - 1, 0, z) * chunk_size, origin=(-0.5, -0.5, -0.5), scale=chunk_size)
            continue
        chunks[x][z] = Entity(x=-1, model=Mesh(vertices=flatten_list(value)), color=color.random_color())

    EditorCamera()
    app.run()
