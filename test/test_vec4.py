from ursina.vec4 import Vec4

class TestVec4:
    def test_multiplying_single_vec4(self):
        sut = Vec4(1, 0, 0, 0)
        assert 2 * sut == Vec4(2, 0, 0, 0)

    def test_multiplying_two_vec4(self):
        sut1 = Vec4(1, 0, 1, 1)
        sut2 = Vec4(2, 1, 2, 3)

        assert sut1 * sut2 == Vec4(2, 0, 2, 3)

    def test_adding_two_vec4(self):
        sut = Vec4(1.252352324, 0, 1, 0.2)
        sut += Vec4(0, 1)
        assert sut == Vec4(1.252352324, 1, 1, 0.2)
