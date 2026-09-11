from ursina import *

def grid_layout(l, max_x=8, spacing=(0,0), origin=(-.5,.5), offset=(0,0), use_abosulte_spacing=False):
    if not isinstance(l, list | tuple):
        print('error: grid_layout input must be a list or tuple, not', l.__class__.__name__)
        return

    spacing = Vec2(*spacing)
    origin = Vec2(*origin)
    offset = Vec2(*offset)


    dimensions = l[0].bounds.size if not use_abosulte_spacing else spacing
    direction = [-e*2 for e in origin]
    direction = Vec2(*[1 if e == 0 else e for e in direction])

    chunked_list = list(chunk_list(l, max_x))

    if origin.y != 0:
        for y, row in enumerate(chunked_list):
            for x, item in enumerate(row):
                item.y = ((y * (dimensions.y + spacing.y)) * direction.y) + (dimensions.y/2 * direction.y) + offset.y
    else:   # center vertically
        total_height = len(chunked_list) * dimensions.y + (len(chunked_list) - 1) * spacing.y
        start_y = -(total_height / 2) + offset.y
        for y, row in enumerate(chunked_list):
            for x, item in enumerate(row):
                item.y = start_y + y * (dimensions.y + spacing.y) + (dimensions.y / 2)

    if origin.x != 0:
        for y, row in enumerate(chunked_list):
            for x, item in enumerate(row):
                item.x = ((x * (dimensions.x + spacing.x)) * direction.x) + (dimensions.x/2 * direction.x) + offset.x

    else:   # center horizontally
        for y, row in enumerate(chunked_list):
            row_width = len(row) * (dimensions.x + spacing.x) - spacing.x
            start_x = -(row_width / 2) + offset.x
            for x, item in enumerate(row):
                item.x = start_x + x * (dimensions.x + spacing.x) + (dimensions.x / 2)
