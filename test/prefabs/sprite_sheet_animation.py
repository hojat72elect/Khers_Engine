from ursina import Ursina, Entity, SpriteSheetAnimation

if __name__ == '__main__':
    '''
    Sprite sheet coordinate system:
    (0,3) (1,3) (2,3) (3,3)
    (0,2) (1,2) (2,2) (3,2)
    (0,1) (1,1) (2,1) (3,1)
    (0,0) (1,0) (2,0) (3,0)
    '''
    app = Ursina()
    player_graphics = SpriteSheetAnimation('sprite_sheet', tileset_size=(4,4), fps=6, animations={
        'idle' : ((0,0), (0,0)),        # makes an animation from (0,0) to (0,0), a single frame
        'walk_up' : ((0,0), (3,0)),     # makes an animation from (0,0) to (3,0), the bottom row
        'walk_right' : ((0,1), (3,1)),
        'walk_left' : ((0,2), (3,2)),
        'walk_down' : ((0,3), (3,3)),
        }
        )
    
    def input(key):
        if key == "w":
            player_graphics.play_animation("walk_up")
        elif key == "s":
            player_graphics.play_animation("walk_down")
        elif key == "d":
            player_graphics.play_animation("walk_right")
        elif key == "a":
            player_graphics.play_animation("walk_left")

    Entity(model='quad', texture='sprite_sheet', x=-1)
    app.run()
