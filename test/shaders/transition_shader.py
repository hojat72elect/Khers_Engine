from ursina import Ursina, window, Texture, Entity, color, load_texture, Slider, EditorCamera, curve
from ursina.shaders.transition_shader import transition_shader

if __name__ == "__main__":
    app = Ursina()
    window.color = color._16
    Texture.default_filtering = "bilinear"
    e = Entity(model="quad", shader=transition_shader, scale=5, cutoff=0, texture="shore", color=color.azure)
    mask = load_texture("shore")
    e.set_shader_input("mask_texture", mask)
    EditorCamera()
    min_cutoff_slider = Slider(0, 1, dynamic=True, y=-0.4)

    def on_value_changed():
        e.set_shader_input("min_cutoff", min_cutoff_slider.value)

    min_cutoff_slider.on_value_changed = on_value_changed
    max_cutoff_slider = Slider(0, 1, default=1, dynamic=True, y=-0.45)

    def on_value_changed():
        e.set_shader_input("max_cutoff", max_cutoff_slider.value)

    max_cutoff_slider.on_value_changed = on_value_changed

    def input(key):
        if key == "space":
            e.cutoff = 0
            e.animate("cutoff", 1, duration=0.1, curve=curve.linear, delay=0.05)

    app.run()
