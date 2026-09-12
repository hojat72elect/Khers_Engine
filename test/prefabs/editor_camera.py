from ursina import Ursina, Sky, load_model, color, Text, window, Button, Entity, EditorCamera

if __name__ == '__main__':
    """
       Simple camera for debugging.
       Hold right click and move the mouse to rotate around point.
    """
    app = Ursina(vsync=False, use_ingame_console=True)
    sky = Sky()
    e = Entity(model=load_model('cube', use_deepcopy=True), color=color.white, collider='box')
    e.model.colorize()
    ground = Entity(model='plane', scale=32, texture='white_cube', texture_scale=(32,32), collider='box')
    box = Entity(model='cube', collider='box', texture='white_cube', scale=(10,2,2), position=(2,1,5), color=color.light_gray)
    b = Button(position=window.top_left, scale=.05)
    editorCamera = EditorCamera(ignore_scroll_on_ui=True)
    rotation_info = Text(position=window.top_left)

    def update():
        rotation_info.text = str(int(editorCamera.rotation_y)) + '\n' + str(int(editorCamera.rotation_x))

    app.run()