from ursina import Ursina, Entity, camera, Animator, Animation, held_keys, time

app = Ursina()
camera.orthographic = True
camera.fov = 9

Entity(model="quad", texture="assets/street", scale=60, z=1)  # background of the game
player = Entity()
anim = Animator(animations={
    "idle": Entity(parent=player, model="cube", texture="assets/walking_0"),
    "walking": Animation("assets/walking", parent=player, autoplay=False)
})


def update():
    if held_keys["w"] or held_keys["a"] or held_keys["s"] or held_keys["d"]:
        anim.state = "walking"
    else:
        anim.state = "idle"

    player.y += held_keys["w"] * 2 * time.dt
    player.y -= held_keys["s"] * 2 * time.dt
    player.x += held_keys["d"] * 2 * time.dt
    player.x -= held_keys["a"] * 2 * time.dt


app.run()
