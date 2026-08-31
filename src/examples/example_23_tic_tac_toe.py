from ursina import Ursina, camera, Text, Entity, color, Tooltip, scene, mouse, Button, Panel

app = Ursina()

camera.orthographic = True
camera.fov = 4
camera.position = (1, 1)
Text.default_resolution *= 2

player = Entity(name="O", color=color.azure)
cursor = Tooltip(player.name, color=player.color, origin=(0, 0), scale=4, enabled=True)
cursor.background.color = color.clear
bg = Entity(parent=scene, model="quad", texture="shore", scale=(16, 8), z=10, color=color.light_gray)
mouse.visible = False

# We create a 3*3 matrix to store the 9 buttons in.
board = [[None for x in range(3)] for y in range(3)]

for y in range(3):
    for x in range(3):
        button = Button(parent=scene, position=(x, y))
        board[x][y] = button


        def on_click(button=button):
            button.text = player.name
            button.color = player.color
            button.collision = False
            check_for_victory()

            if player.name == "O":
                player.name = "X"
                player.color = color.orange
            else:
                player.name = "O"
                player.color = color.azure

            cursor.text = player.name
            cursor.color = player.color


        button.on_click = on_click


def check_for_victory():
    prospective_winner = player.name

    did_win = ((board[0][0].text == prospective_winner and board[1][0].text == prospective_winner and board[2][0].text == prospective_winner) or
               (board[0][1].text == prospective_winner and board[1][1].text == prospective_winner and board[2][1].text == prospective_winner) or
               (board[0][2].text == prospective_winner and board[1][2].text == prospective_winner and board[2][2].text == prospective_winner) or
               (board[0][0].text == prospective_winner and board[0][1].text == prospective_winner and board[0][2].text == prospective_winner) or
               (board[1][0].text == prospective_winner and board[1][1].text == prospective_winner and board[1][2].text == prospective_winner) or
               (board[2][0].text == prospective_winner and board[2][1].text == prospective_winner and board[2][2].text == prospective_winner) or
               (board[0][0].text == prospective_winner and board[1][1].text == prospective_winner and board[2][2].text == prospective_winner) or
               (board[0][2].text == prospective_winner and board[1][1].text == prospective_winner and board[2][0].text == prospective_winner))

    if did_win:
        print(f"Winner is :{prospective_winner}")
        cursor.text = ""
        mouse.visible = True
        Panel(z=1, scale=10, model="quad")
        text = Text(f"player\n{prospective_winner}\nwon!", scale=3, origin=(0,0), background=True)
        text.create_background(padding=(0.5, 0.25), radius=Text.size/2)
        text.background.color = player.color.tint(-0.2)


app.run()
