from random import choice
from examples.example_26_inventory.Inventory import Inventory
from ursina import Ursina, Button, color, Tooltip, Entity, camera, Cursor, mouse

if __name__ == '__main__':
    app = Ursina()
    inventory = Inventory()

    def add_item():
        inventory.append(choice(("bag", "bow_arrow", "gem", "orb", "sword")))

    add_item()
    add_item()
    add_item_button = Button(scale=(0.1, 0.1), x=-0.5, color=color.lime.tint(-0.25), text="+", tooltip=Tooltip("Add random item"), on_click=add_item)
    background = Entity(parent=camera.ui, model="quad", texture="shore", scale_x=camera.aspect_ratio, z=1)
    Cursor(texture="cursor", scale=0.1)
    mouse.visible = False
    app.run()
