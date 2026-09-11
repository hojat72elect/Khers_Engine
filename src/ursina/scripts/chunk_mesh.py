
from math import ceil, floor

from ursina.array_tools import Array2D, chunk_list, enumerate_2d
from ursina.ursinamath import clamp

def chunk_mesh(mesh, num_chunks, chunk_size=1/8):
    if not hasattr(mesh, 'vertices'):
        raise Exception(f'{mesh} has no vertices')

    chunks = Array2D(width=num_chunks[0], height=num_chunks[1])
    for (x,z), _value in enumerate_2d(chunks):
        chunks[x][z] = []

    polys = list(chunk_list(mesh.generated_vertices, 3))

    for i, tri in enumerate(polys):
        if chunk_size >= 1:
            min_x = floor(min(v.x for v in tri) / chunk_size)
            min_y = floor(min(v.z for v in tri) / chunk_size)
            max_x = ceil(max(v.x for v in tri) / chunk_size)
            max_y = ceil(max(v.z for v in tri) / chunk_size)
        else:
            min_x = floor(min(v.x for v in tri) / chunk_size)
            min_y = floor(min(v.z for v in tri) / chunk_size)
            max_x = ceil(max(v.x for v in tri) / chunk_size)
            max_y = ceil(max(v.z for v in tri) / chunk_size)

        min_x = clamp(min_x, 0, chunks.width-1)
        max_x = clamp(max_x, 0, chunks.width-1)
        min_y = clamp(min_y, 0, chunks.height-1)
        max_y = clamp(max_y, 0, chunks.height-1)

        # print(min_x, max_x, min_y, max_y)
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                # print('append tri', i, 'to chunk', x, y)
                chunks[x][y].append(tri)

    return chunks
