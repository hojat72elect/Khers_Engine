from ursina import Entity, color, camera, Ursina, Quad, after

app = Ursina()
size = 32
plane = Entity(model='quad', color=color.azure, origin=(-.5, -.5), z=10, collider='box', scale=size)  # create an invisible plane for the mouse to collide with
grid = [[Entity(model='quad', position=(x, y), texture='white_cube', enabled=False) for y in range(size)] for x in range(size)]  # make 2d array of entities
cursor = Entity(model=Quad(mode='line'), color=color.lime)

class Player(Entity):
    def __init__(self):
        super().__init__(model='quad', color=color.orange, position=(16, 16, -.1))

    def input(self, key):
        if key in ('a', 'a hold'):
            self.walk(-1)
        if key in ('d', 'd hold'):
            self.walk(1)
        if key == 's':
            grid[int(self.x)][int(self.y) - 1].enabled = False
            self.fall()
        if key == 'space':
            grid[int(self.x)][int(self.y)].enabled = True
            self.y += 1

    def fall(self):
        dist = 0
        l = 0
        for i in range(1, size):
            print(i)
            if grid[self.X][self.Y - i].enabled:
                break
            l += 1
        if not l:
            return
        self.ignore_input = True
        self.animate('y', self.y - l, duration=.1)

        @after(.101)
        def _():
            self.ignore_input = False

    def walk(self, dir):
        if not grid[self.X + dir][self.Y + 1].enabled:  # remove block of there's not a block above it
            grid[self.X + dir][self.Y].enabled = False
        if not grid[self.X + dir][self.Y].enabled:
            self.x += dir
            self.fall()

player = Player()
camera.orthographic = True
camera.fov = 10
camera.position = (16, 18)
# enable all tiles lower than 16 to make a ground
for column in grid:
    for e in column:
        if e.y <= 15:
            e.enabled = True

app.run()
