from ursina import Ursina, Func, Text, ButtonList

if __name__ == '__main__':    
    app = Ursina()
    default = Func(print, 'not yet implemented')
    
    def exampleFunc(a=1, b=2):
        print('------:', a, b)

    button_dict = {}
    for i in range(6, 20):
        button_dict[f'button {i}'] = Func(print, i)

    bl = ButtonList(button_dict, font=Text.default_monospace_font, button_height=1.5, popup=0, clear_selected_on_enable=False, clear_selected_on_click_outside=False)
    
    def input(key):
        if key == 'space':
            bl.button_dict = {
                "one": None,
                "two": default,
                "tree": Func(exampleFunc, 3, 4),
                "four": Func(exampleFunc, b=3, a=4),
            }
        if key == 'o':
            bl.enabled = True

    bl.selected = 'button 7'
    bl.button_dict = {}
    app.run()
