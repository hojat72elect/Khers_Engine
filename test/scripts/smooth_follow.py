from ursina import EditorCamera, Entity, Ursina, color, held_keys
from ursina.scripts.smooth_follow import SmoothFollow

if __name__ == "__main__":
    app = Ursina()
    player = Entity(model="cube", color=color.orange)

    def update():
        player.x += held_keys["d"] * 0.1
        player.x -= held_keys["a"] * 0.1

    e = Entity(model="cube")
    sf = e.add_script(SmoothFollow(target=player, offset=(0, 2, 0)))

    def input(key):
        global sf
        if key == "1" and sf in e.scripts:
            e.scripts.remove(sf)

    EditorCamera()
    app.run()
