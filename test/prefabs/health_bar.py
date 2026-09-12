from ursina import Ursina, color
from ursina.prefabs.health_bar import HealthBar

if __name__ == "__main__":
    app = Ursina()
    health_bar_1 = HealthBar(bar_color=color.lime.tint(-0.25), roundness=0.5, max_value=100, value=50, scale=(0.5, 0.1))
    print(health_bar_1.text_entity.enabled, health_bar_1.text_entity.text)

    def input(key):
        if key == "+" or key == "+ hold":
            health_bar_1.value += 10
        if key == "-" or key == "- hold":
            health_bar_1.value -= 10
            print("ow")

    app.run()
