from ursina import Ursina, every, Entity

if __name__ == '__main__':
    app = Ursina()

    class Enemy(Entity):
        @every(0.2)
        def attack(self):
            print("attack")

    enemy = Enemy(enabled=1)

    # It gets paused when disabling the entity.
    def input(key):
        if key == "space":
            enemy.enabled = not enemy.enabled
            print(enemy.enabled)

    app.run()
