from ursina import Ursina, Entity, InputField, color, Button, camera

if __name__ == '__main__':
    app = Ursina()
    gradient = Entity(model='quad', texture='vertical_gradient', parent=camera.ui, scale=(camera.aspect_ratio,1), color=color.hsv(240,.6,.1,.75))
    username_field = InputField(y=-.12, limit_content_to='0123456789', default_value='11', active=True, scale_x=1)
    username_field.text = '0929468098'
    password_field = InputField(y=-.18, hide_content=True)
    username_field.next_field = password_field

    def submit():
        print('ursername:', username_field.text)
        print('password:',  password_field.text)

    Button(text='Login', scale=.1, color=color.cyan.tint(-.4), y=-.26, on_click=submit).fit_to_text()
    username_field.on_value_changed = submit
    app.run()