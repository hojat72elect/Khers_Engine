from ursina.mesh import Mesh
from ursina import color
from ursina.entity import Entity
from ursina.vec2 import Vec2
from ursina.vec3 import Vec3
from ursina.prefabs.sky import Sky
from ursina.main import Ursina
from ursina.texture import Texture
from ursina.texture_importer import load_texture
from ursina.prefabs.editor_camera import EditorCamera
import time

class Terrain(Mesh):
    def __init__(self, heightmap, skip=1, **kwargs):
        from PIL import Image
        from numpy import asarray, flip, swapaxes

        self.heightmap = heightmap

        if not isinstance(heightmap, Texture):
            self.heightmap = load_texture(heightmap)
            if not self.heightmap:
                print('failed to load heightmap:', heightmap)
                return

        self.skip = skip    # should be power of two.
        self.width, self.depth = self.heightmap.width//skip, self.heightmap.height//skip
        self.aspect_ratio = self.width / self.depth

        img = Image.open(self.heightmap.path).convert('L')
        if self.skip > 1:
            img = img.resize([self.width, self.depth], Image.Resampling.LANCZOS)

        self.height_values = asarray(img)
        self.height_values = flip(self.height_values, axis=0)
        self.height_values = swapaxes(self.height_values, 0, 1)

        # copy this from Plane to avoid unnecessary init
        self.vertices, self.triangles = list(), list()
        self.uvs = list()
        self.normals = list()
        w, h = self.width, self.depth
        self.height_values = [[j/255 for j in i] for i in self.height_values]


        centering_offset = Vec2(-.5, -.5)
        if self.aspect_ratio > 1: # offset should be different if the terrain is not 1:1
            centering_offset.x *= self.aspect_ratio
        else:
            centering_offset.y /= self.aspect_ratio

        min_dim = min(w, h)


        # create the plane
        i = 0
        for z in range(h+1):
            for x in range(w+1):
                y = self.height_values[x - (x == w)][z - (z == h)]  # do -1 if the coordinate is not in range

                self.vertices.append(Vec3((x/min_dim)+(centering_offset.x), y, (z/min_dim)+centering_offset.y))
                self.uvs.append((x/w, z/h))

                if x > 0 and z > 0:
                    self.triangles.append((i, i-1, i-w-2, i-w-1))

                # normals
                if 0 < x < w - 1 and 0 < z < h - 1:
                    rl = self.height_values[x + 1][z] - self.height_values[x - 1][z]
                    fb = self.height_values[x][z + 1] - self.height_values[x][z - 1]
                    self.normals.append(Vec3(rl, 1, fb).normalized())
                else:
                    self.normals.append(Vec3(0,1,0))

                i += 1

        super().__init__(vertices=self.vertices, triangles=self.triangles, uvs=self.uvs, normals=self.normals, **kwargs)

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model=Terrain('heightmap_1', skip=16), scale=(20,5,20), texture='heightmap_1')
    Entity(model='plane', scale=e.scale, color=color.red)
    EditorCamera()
    Sky()

    # test
    t = time.time()
    e.collider = 'mesh'
    print(time.time() - t)

    def input(key):
        if key == '-':
            e.scale *= .9

    app.run()
