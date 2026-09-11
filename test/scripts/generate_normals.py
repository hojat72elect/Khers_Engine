from time import perf_counter
from ursina.scripts.generate_normals import generate_normals

if __name__ == '__main__':
    vertices = (
        (-0.0, -0.5, 0.0), (0.1, -0.48, -0.073), (-0.038, -0.48, -0.11),
        (0.361804, -0.22, -0.26), (0.3, -0.32, -0.22), (0.40, -0.25, -0.14),
        (-0.0, -0.5, 0.0), (-0.038, -0.48, -0.11), (-0.03, -0.48, -0.11)
    )

    t = perf_counter()
    norms = generate_normals(vertices, smooth=True)
    print('------', perf_counter() - t)