from ursina import Ursina, window, mouse, color, Entity, lerp, EditorCamera, Grid, destroy, time
from ursina.prefabs.trail_renderer import TrailRenderer

if __name__ == '__main__':
    app = Ursina(vsync=False)
    window.color = color.black
    mouse.visible = False
    player = Entity(z=1)
    player.graphics = Entity(parent=player, scale=.1, model='circle')

    pivot = Entity()

    trail_renderers = []
    for i in range(1):
        tr = TrailRenderer(size=[1,1], segments=8, min_spacing=.2, fade_speed=0, parent=player, color_gradient=[color.magenta, color.cyan.tint(-.5), color.clear])
        trail_renderers.append(tr)

    def update():
        player.position = lerp(player.position, mouse.position*10, time.dt*4)


    def input(key):
        if key == 'escape':
            for e in trail_renderers:
                e.enabled = not e.enabled

        if key == 'space':
            destroy(pivot)

    EditorCamera()
    Entity(model=Grid(8,8), rotation_x=90, color=color.gray, y=-3, scale=8)
    app.run()
