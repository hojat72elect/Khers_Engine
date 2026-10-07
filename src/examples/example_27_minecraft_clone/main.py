from examples.example_27_minecraft_clone.Voxel import Voxel
from ursina import application
from ursina.main import Ursina
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.sky import Sky
from ursina.destroy import destroy
from ursina.raycast import raycast
from ursina.mouse import instance as mouse
from ursina.camera import instance as camera

if __name__ == '__main__':
    app = Ursina()

    for z in range(8):
        for x in range(8):
            voxel = Voxel(position=(x, 0, z))

    def input(key):
        if key == 'escape':
            application.quit()
        if key == 'left mouse down':
            hit_info = raycast(camera.world_position, camera.forward, distance=5)
            if hit_info.hit:
                Voxel(position=hit_info.entity.position + hit_info.normal)
        if key == 'right mouse down' and mouse.hovered_entity:
            destroy(mouse.hovered_entity)

    Sky()
    FirstPersonController()
    app.run()
