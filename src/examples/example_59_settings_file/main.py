from ursina import application, Button, Text, Ursina
from pathlib import Path

if __name__ == '__main__':
    print('--------', application.asset_folder)
    application.asset_folder = Path(application.asset_folder / 'test')
    app = Ursina()

    Button('Here is some text').fit_to_text()
    Text('Make a file called "ursina_settings.py" in the root folder and \nthe engine will run the code in it.', y=.4, z=-1, origin=(0, 0))

    app.run()
