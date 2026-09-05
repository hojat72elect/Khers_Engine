from ursina import Entity, Ursina, Sequence, Func, Wait

if __name__ == '__main__':
    app = Ursina()
    e = Entity(model='quad')
    
    def some_func():
        print('some_func')
        
    s = Sequence(some_func, 1, Func(print, 'one'), Func(e.fade_out, duration=1), Wait(1), loop=True)

    for i in range(8):
        s.append(Func(print, i))
        s.append(Wait(.2))
    print(s)

    def input(key):
        actions = {"s": s.start, "f": s.finish, "p": s.pause, "r": s.resume}
        if key in actions:
            actions[key]()

    app.run()
