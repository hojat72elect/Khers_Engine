from ursina import application

from example_1.Example1 import Example1

if __name__ == '__main__':
    game = Example1()


    def update():
        game.listenToInputs()
        game.handleCollisions()


    def input(key):
        if key == 'escape':
            application.quit()
        if key == 'f':
            game.clank_sound.play()


    game.run()
