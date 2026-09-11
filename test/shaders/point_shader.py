import random

from ursina import EditorCamera, Entity, Mesh, MeshModes, Ursina, Vec3, color
from ursina.prefabs.primitives import ThinSlider
from ursina.shaders.point_shader import point_shader

if __name__ == "__main__":
    app = Ursina(vsync=1)
    Entity(model="plane", scale=10, texture="grass")

    vertices = [Vec3(*(random.random() * 10 for _ in range(3))) for i in range(100)]
    e = Entity(
        model=Mesh(
            mode=MeshModes.point,
            vertices=vertices,
            colors=[color.random_color() for _ in vertices],
            render_points_in_3d=False,
            thickness=0.001,
        ),
        shader=point_shader,
        texture="circle",
    )
    e2 = Entity(
        model=Mesh(
            mode=MeshModes.point,
            vertices=vertices,
            colors=[color.random_color() for _ in vertices],
            render_points_in_3d=True,
            thickness=1,
        ),
        shader=point_shader,
        texture="radial_gradient",
        x=10,
    )
    e2_bounds = Entity(
        model="wireframe_cube",
        color=color.green,
        position=e2.position,
        origin=(-0.5, -0.5, -0.5),
        scale=10,
    )

    slider = ThinSlider(text="thickness", min=1, max=32, default=1)

    def _set_point_size():
        e.set_shader_input("thickness", slider.value)
        e2.set_shader_input("thickness", slider.value)
        print("set thickness to:", slider.value, e.get_shader_input("thickness"))

    slider.on_value_changed = _set_point_size
    Entity(model="sphere", wireframe=True, origin_y=-0.5)
    EditorCamera()
    app.run()
