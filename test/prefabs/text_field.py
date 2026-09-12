from ursina import Ursina, window, Button, color, TextField
from textwrap import dedent

if __name__ == '__main__':
    app = Ursina(vsync=60)
    window.color = color.hsv(0, 0, .1)
    Button.default_color = color._20
    window.color = color._25
    te = TextField(max_lines=30, scale=1, register_mouse_input = True, text='1234')
    te.text = dedent('''
        Lorem ipsum dolor sit amet, consectetur adipiscing elit.
        Aliquam sapien tellus, venenatis sit amet ante et, malesuada porta risus.
        Etiam et mi luctus, viverra urna at, maximus eros. Sed dictum faucibus purus,
        nec rutrum ipsum condimentum in. Mauris iaculis arcu nec justo rutrum euismod.
        Suspendisse dolor tortor, congue id erat sit amet, sollicitudin facilisis velit.
        Aliquam sapien tellus, venenatis sit amet ante et, malesuada porta risus.
        Etiam et mi luctus, viverra urna at, maximus eros. Sed dictum faucibus purus,
        nec rutrum ipsum condimentum in. Mauris iaculis arcu nec justo rutrum euismod.
        Suspendisse dolor tortor, congue id erat sit amet, sollicitudin facilisis velit.
        '''*30
        )[1:]
    te.render()

    def input(key):
        if key == '3':
            te.input('scroll down')

    app.run()
