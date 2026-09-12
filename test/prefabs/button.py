from ursina import Ursina, Button, color, NineSlice, Func, Wait, Sequence, camera, application, Tooltip, Entity, Audio, Text, scene, Sky

if __name__ == "__main__":
    app = Ursina()
    Button.default_color = color.white
    Button.default_model = NineSlice
    Button.default_texture = "nineslice_rainbow"
    Button.default_radius = 0.5
    b = Button(
        model="quad",
        scale=0.05,
        x=-0.5,
        color=color.lime,
        text="text_size\ntest",
        text_size=0.5,
        text_color=color.black,
    )
    b.on_click = Sequence(Wait(0.5), Func(print, "aaaaaa"))

    b1 = Button(parent=camera.ui, text="hello world!", scale=0.25)
    b2 = Button(text="hello world!", icon="sword", scale=0.25, text_origin=(-0.5, 0), x=0.5)
    b2.on_click = application.quit
    b2.tooltip = Tooltip("exit")
    par = Entity(parent=camera.ui, scale=0.2, y=-0.2)
    b3 = Button(parent=par, text="test", scale_x=1, origin=(-0.5, 0.5))
    b3.text = "new text"
    print(b.text_entity)

    Button(
        text="sound",
        scale=0.2,
        position=(-0.25, -0.2),
        color=color.pink,
        highlight_sound="blip_1",
        pressed_sound=Audio("coin_1", autoplay=False),
    )

    Button(
        "highlight\ntest",
        scale=(0.2, 0.1),
        highlight_color=color.magenta,
        highlight_text_color=color.cyan,
        highlight_scale=1.2,
        highlight_text_size=1.2,
        position=0.2,
    )
    Text("Text size\nreference", x=0.15)

    def input(key):
        if key == "d":
            scene.clear()
        if key == "space":
            b.text = "updated text"

    Sky()
    app.run()
