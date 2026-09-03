from random import random
from ursina import Entity, camera, Quad, color, Text, destroy, Draggable, Tooltip

class Inventory(Entity):
    def __init__(self, width=5, height=8, **kwargs):
        super().__init__(
            parent=camera.ui,
            model=Quad(radius=0.015),
            texture="white_cube",
            texture_scale=(width, height),
            scale=(0.1 * width, 0.1 * height),
            origin=(-0.5, 0.5),
            position=(-0.3, 0.4),
            color=color.hsv(0, 0, 0.1, 0.9)
        )

        self.width = width
        self.height = height

        for key, value in kwargs.items():
            setattr(self, key, value)

    def find_free_spot(self):
        for y in range(self.height):
            for x in range(self.width):
                grid_positions = [(int(e.x * self.texture_scale[0]), int(e.y * self.texture_scale[1])) for e in self.children]
                print(grid_positions)

                if not (x, -y) in grid_positions:
                    print(f"found free spot : {x} , {y}")
                    return x, y

    def append(self, item, x=0, y=0):
        print(f"add item : {item}")

        if len(self.children) >= self.width * self.height:
            print("Inventory is full")
            error_message = Text("<red>Inventory is full!", origin=(0, -1.5), x=-0.5, scale=2)
            destroy(error_message, delay=1)
            return

        x, y = self.find_free_spot()
        icon = Draggable(
            parent=self,
            model="quad",
            texture=item,
            color=color.white,
            scale_x=1 / self.texture_scale[0],
            scale_y=1 / self.texture_scale[1],
            origin=(-0.5, 0.5),
            x=x * 1 / self.texture_scale[0],
            y=-y * 1 / self.texture_scale[1],
            z=-1
        )
        name: str = item.replace("_", " ").title()

        if random() < 0.25:
            icon.color = color.gold
            name = f"<orange>Rare {name}"

        icon.tooltip = Tooltip(name)
        icon.tooltip.background_entity.color = color.hsv(0, 0, 0, 0.8)

        def drag():
            icon.org_pos = (icon.x, icon.y)
            icon.z = -2

        def drop():
            icon.x = int((icon.x + (icon.scale_x / 2)) * self.width) / self.width
            icon.y = int((icon.y - (icon.scale_y / 2)) * self.height) / self.height
            icon.z = -1

            # If the item was dropped outside the grid, will return to the original position
            if icon.x < 0 or icon.x >= 1 or icon.y > 0 or icon.y <= -1:
                icon.position = (icon.org_pos)
                return

            # If the spot is taken, the items will swap their positions with each other
            for child in self.children:
                if child == icon:
                    continue

                if child.x == icon.x and child.y == icon.y:
                    print("Swap positions")
                    child.position = icon.org_pos

        icon.drag = drag
        icon.drop = drop
