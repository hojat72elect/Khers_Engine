from ursina import window, application,Ursina, color, scene

if __name__ == "__main__":

    application.trace_entity_definition = True
    app = Ursina(title="Ursina", vsync=False)

    def input(key):
        if key == "space":
            window.center_on_screen()
        if key == "p":
            for e in scene.entities:
                if not e.eternal:
                    print(e.name)

    window.color = color.white
    app.run()
