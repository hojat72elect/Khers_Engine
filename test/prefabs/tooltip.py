from ursina import Ursina, Tooltip, NineSlice, Vec2, Text, color

if __name__ == "__main__":
    app = Ursina()

    tooltip_test = Tooltip(
        "<scale:1.5><pink>"
        + "Rainstorm"
        + "<scale:1> \n \n"
        + """Summon a <blue>rain
storm <default>to deal 5 <blue>water
damage <default>to <red>everyone, <default>including <orange>yourself. <default>
Lasts for 4 rounds.""".replace("\n", " "),
        background_color=color.white,
        background_model_class=NineSlice,
        background_radius=0.25,
        padding=Vec2(0.1),
        font=Text.default_monospace_font,
        wordwrap=50,
    )
    tooltip_test.background_entity.texture = "nineslice_rainbow"
    tooltip_test.enabled = True
    app.run()
