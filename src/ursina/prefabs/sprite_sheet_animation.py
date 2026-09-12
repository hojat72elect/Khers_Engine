from ursina import Entity, Sequence, Func, Wait

class SpriteSheetAnimation(Entity):
    def __init__(self, texture, animations, tileset_size=[4,1], fps=12, model='quad', autoplay=True, **kwargs):
        kwargs['model'] = model
        kwargs['texture'] = texture
        kwargs['tileset_size'] = tileset_size
        super().__init__(**kwargs)

        self.animations = animations # should be a dict

        for key, value in self.animations.items():
            start_coord, end_coord = value
            s = Sequence(loop=True)

            for y in range(start_coord[1], end_coord[1]+1):
                for x in range(start_coord[0], end_coord[0]+1):
                    s.extend([
                        Func(setattr, self, 'tile_coordinate', (x,y)),
                        Wait(1/fps)
                    ])
            self.animations[key] = s


    def play_animation(self, animation_name):
        if not self.animations:
            return

        [anim.pause() for anim in self.animations.values()]

        self.animations[animation_name].start()
