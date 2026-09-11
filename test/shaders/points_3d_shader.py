import random
from ursina import EditorCamera, Entity, Mesh, MeshModes, Ursina, Vec3, camera, color
from ursina.prefabs.primitives import ThinSlider
from ursina.shaders.points_3d_shader import unlit_points_shader

if __name__ == "__main__":
    app = Ursina(vsync=1)
    camera.clip_plane_near = 1
    Entity(model="plane", scale=10, texture="grass")

    vertices = [Vec3(*(random.random() * 10 for _ in range(3))) for i in range(100)]
    e = Entity(
        model=Mesh(
            mode=MeshModes.point,
            vertices=vertices,
            colors=[color.random_color() for _ in vertices],
            render_points_in_3d=True,
            thickness=50,
        ),
        shader=unlit_points_shader,
        texture="circle",
    )

    slider = ThinSlider(text="point_size", min=1, max=32, default=4)

    def _set_point_size():
        e.set_shader_input("point_size", slider.value)
        print("set point_size to:", slider.value, e.get_shader_input("point_size"))

    slider.on_value_changed = _set_point_size
    EditorCamera()
    app.run()
