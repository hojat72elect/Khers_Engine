from ursina import music_system, Ursina, ButtonGroup, Text

if __name__ == '__main__':
    app = Ursina()
    music_changer = ButtonGroup(('', 'crestlands_part', 'dunes_part'), label='music')

    def on_music_selected():
        music_system.play(music_changer.value if music_changer.value != 'None' else None)

    music_changer.on_value_changed = on_music_selected
    ambiance_changer = ButtonGroup(('', 'noise', 'square'), label='ambiance', y=-.1)

    def on_ambiance_selected():
        music_system.play_ambiance(ambiance_changer.value if ambiance_changer.value != 'None' else None)

    ambiance_changer.on_value_changed = on_ambiance_selected
    t = Text('SPACE: Toggle music\nA: Toggle ambiance', origin=(0, 0), y=-.4)

    def update():
        t.text = f'''\
            current_music_track:    {music_system.current_music_track},
            prev_music_track: {music_system.prev_music_track},

            current_ambiance_track: {music_system.current_ambiance_track},
            prev_ambiance_track: {music_system.prev_ambiance_track},
            '''

    app.run()
