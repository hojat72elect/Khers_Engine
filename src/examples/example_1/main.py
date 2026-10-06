from examples.example_1.Example1 import Example1
from ursina.application import quit

if __name__ == '__main__':
    game = Example1()

    def update():
        game.listenToInputs()
        game.handleCollisions()

    def input(key):
        if key == 'escape':
            quit()
        if key == 'f':
            game.clank_sound.play()

    game.run()
