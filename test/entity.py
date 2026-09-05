from ursina import Ursina, Entity, DirectionalLight, Vec3, EditorCamera, color, scene, shaders

if __name__ == '__main__':
    
    app = Ursina()
    ground = Entity(model='plane', texture='grass', scale=10, shader=shaders.lit_with_shadows_shader)
    e = Entity(model='cube', y=1, texture='grass')

    DirectionalLight().look_at(Vec3(1,-1,.5))
    EditorCamera(rotation_x=15)
    scene.fog_color = color.blue
    scene.fog_density = (0,100)

    app.run()
