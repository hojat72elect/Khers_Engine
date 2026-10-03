from ursina import color

class TestColor:
    def test_general_behavior(self):
        assert color.hsv(30, 1, 1) == color.orange
        assert color.brightness(color.blue) == 1.0
        assert color.red.rgb == (1.0, 0.0, 0.0)
        assert color.red.rgba == (1.0, 0.0, 0.0, 1.0)
