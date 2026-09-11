from ursina import inverselerp, lerp

class TestUrsinaMath:
    def test_general_math(self):
        assert inverselerp(0, 100, 50) == 0.5
        assert lerp(0, 100, 0.5) == 50
