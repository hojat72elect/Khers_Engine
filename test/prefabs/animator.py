from ursina import Ursina, Animation, Entity, color, Text, Animator

if __name__ == '__main__':
    app = Ursina()
    anim = Animation('ursina_wink', loop=True, autoplay=False)
    a = Animator(
        animations={
            "lol": Entity(model="cube", color=color.red),
            "yo": Entity(model="cube", color=color.green, x=1),
            "help": anim,
        }
    )
    a.state = 'yo'
    Text('press <red>1<default>, <green>2<default> or <violet>3<default> to toggle different animator states', origin=(0,-.5), y=-.4)

    def input(key):
        if key == '1':
            a.state = 'lol'
        if key == '2':
            a.state = 'yo'
        if key == '3':
            a.state = 'help'
            print(anim.enabled)

    app.run()
