import random

from ursina import Ursina, Entity, camera, Animator, Animation, held_keys, time, Sprite, SmoothFollow

app = Ursina()
camera.orthographic = True
camera.fov = 9

npcs = []
for i in range(12):
    if i < 6:
        rot = 180
        val = -1
    else:
        rot = 0
        val = 1
    npc = Animation("assets/npc", autoplay=True, rotation=rot, scale=0.75, position=(random.randint(-22, 22), random.randint(-22, 22)), collider="box", tag="npc")
    npcs.append((npc, val))

Entity(model="quad", texture="assets/street", scale=60, z=1)  # background of the game
player = Entity()
anim = Animator(animations={
    "idle": Entity(parent=player, model="cube", texture="assets/walking_0"),
    "walking": Animation("assets/walking", parent=player, autoplay=False)
})

for i in [-8, 8]:
    for j in [-2, 4]:
        Sprite(model="cube", texture="assets/house", scale=0.75, collider="box", position=(i, j, 0), rotation_z=0 if i == -8 else 180)

for i in [-2.5, 2.5]:
    for j in [-3.5, 6]:
        Sprite(model="cube", texture="assets/house", scale=0.75, collider="box", position=(i, j, 0), rotation_z=270 if j == -3.5 else 90)

follow = SmoothFollow(target=player, speed=8, offset=[0,0,-4])
camera.add_script(follow)

def update():
    for npc, val in npcs:
        npc.y += val * time.dt
        if val == 1:
            if npc.y > 22:
                npc.y = -22
        else:
            if npc.y < -22:
                npc.y = 22

    if held_keys["w"] or held_keys["a"] or held_keys["s"] or held_keys["d"]:
        anim.state = "walking"
    else:
        anim.state = "idle"

    player.y += held_keys["w"] * 2 * time.dt
    player.y -= held_keys["s"] * 2 * time.dt
    player.x += held_keys["d"] * 2 * time.dt
    player.x -= held_keys["a"] * 2 * time.dt
    if held_keys["s"]:
        player.rotation_z = 180
    if held_keys["w"]:
        player.rotation_z = 0
    if held_keys["d"]:
        player.rotation_z = 90
    if held_keys["a"]:
        player.rotation_z = 270
    if held_keys["w"] and held_keys["d"]:
        player.rotation_z = 45
    if held_keys["w"] and held_keys["a"]:
        player.rotation_z = 315
    if held_keys["a"] and held_keys["s"]:
        player.rotation_z = 225
    if held_keys["d"] and held_keys["s"]:
        player.rotation_z = 135


app.run()
