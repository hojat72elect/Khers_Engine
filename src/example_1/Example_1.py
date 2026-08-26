from ursina import Ursina, Entity, color, Text, Audio, held_keys, time, mouse, application

app = Ursina()

movement_speed = 5
background = Entity(model='quad', scale=(16, 16), color=color.white, z=1)
potato = Entity(model='quad', texture='assets/potato.png', scale=(0.5, 0.5), position=(-5, 0, 0), collider='box')
target = Entity(model='quad', scale=(160 / 40, 280 / 40), position=(1.5, 1.5, 0), color=color.black, collider='box')
hello_text = Text(text='Hello World!', position=(0.0, 0.15), origin=(0, 0), color=color.black, scale=1.5)
clank_sound = Audio('assets/clank.wav', autoplay=False)
potato_collision = False
mouse_collision = False


def update():
    global potato_collision, mouse_collision
    if held_keys['d']:
        potato.x += movement_speed * time.dt
    if held_keys['a']:
        potato.x -= movement_speed * time.dt
    if held_keys['w']:
        potato.y += movement_speed * time.dt
    if held_keys['s']:
        potato.y -= movement_speed * time.dt

    hit_info = potato.intersects(target)
    potato_collision = hit_info.hit
    mouse_collision = mouse.hovered_entity == target

    if potato_collision and mouse_collision:
        target.color = color.yellow
    elif potato_collision:
        target.color = color.red
    elif mouse_collision:
        target.color = color.blue
    else:
        target.color = color.black


def input(key):
    if key == 'escape':
        application.quit()
    if key == 'f':
        clank_sound.play()


if __name__ == '__main__':
    app.run()
