from ursina import Ursina, Entity, Vec3, time, held_keys, terraincast, Terrain, color, EditorCamera, Sky

if __name__ == '__main__':
    app = Ursina()
    terrain_entity = Entity(model=Terrain('heightmap_1', skip=8), scale=(40, 5, 20), texture='heightmap_1')
    player = Entity(model='sphere', color=color.azure, scale=.2, origin_y=-.5)
    normal_indicator = Entity(model='arrow', color=color.cyan, parent=player, y=1, origin_x=-.5)
    hv = terrain_entity.model.height_values

    def update():
        direction = Vec3(held_keys['d'] - held_keys['a'], 0, held_keys['w'] - held_keys['s']).normalized()
        player.position += direction * time.dt * 4
        y, normal = terraincast(player.world_position, terrain_entity, hv, return_normals=True)
        if y is not None:
            player.y = y
            normal_indicator.look_in_direction(normal, Vec3.right)

    EditorCamera()
    Sky()
    app.run()
