from ursina import Ursina, Entity, held_keys, time, duplicate, camera, EditorCamera, Vec3, color, raycast

if __name__ == '__main__':
    app = Ursina()
    '''
    Casts a ray from *origin*, in *direction*, with length *distance* and returns
    a HitInfo containing information about what it hit. This ray will only hit entities with a collider.

    Use optional *traverse_target* to only be able to hit a specific entity and its children/descendants.
    Use optional *ignore* list to ignore certain entities.
    Setting debug to True will draw the line on screen.

    Example where we only move if a wall is not hit:
    '''
    class Player(Entity):

        def update(self):
            self.direction = Vec3(
                self.forward * (held_keys['w'] - held_keys['s'])
                + self.right * (held_keys['d'] - held_keys['a'])
                ).normalized()  # get the direction we're trying to walk in.

            origin = self.world_position + (self.up*.5)  # the ray should start slightly up from the ground so we can walk up slopes or walk over small objects.
            hit_info = raycast(origin, self.direction, ignore=(self,), distance=0.5, debug=False)
            if not hit_info.hit:
                self.position += self.direction * 5 * time.dt
            else:
                print(hit_info.entity)

    Player(model='cube', origin_y=-.5, color=color.orange)
    wall_left = Entity(model='cube', collider='box', scale_y=3, origin_y=-.5, color=color.azure, x=-4)
    wall_right = duplicate(wall_left, x=4)
    camera.y = 2
    app.run()
    EditorCamera()
    
    app.run()
