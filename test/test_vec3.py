import math
from ursina import Vec2, Vec3

class TestVec3:
    def test_multiplying_single_vec3(self):
        sut = Vec3(1, 0, -1)
        assert 2 * sut == Vec3(2, 0, -2)

    def test_multiplying_two_vec3(self):
        sut1 = Vec3(1, 0, -1)
        sut2 = Vec3(1, 2, 3)
        assert sut1 * sut2 == Vec3(1, 0, -3)

    def test_adding_two_vec3(self):
        sut = Vec3(1, 0, 1)
        sut += Vec3(0, 1, 0)
        assert sut == Vec3(1, 1, 1)

    def test_plus_equal_int(self):
        sut = Vec3(0, 0, 0)
        sut.x += 1
        sut.y += 1
        sut.z += 1
        assert sut == Vec3(1, 1, 1)

    def test_round_vec3(self):
        sut = Vec3(1.14, 2.86, 1.25)
        assert round(sut, 0) == Vec3(1, 3, 1)

    def test_abs_vec3(self):
        sut = Vec3(1, -2, -3)
        assert abs(sut) == Vec3(1, 2, 3)

    def test_general_behavior(self):
        sut = Vec3(1.1, 2.5, 3.4)

        assert math.isclose(sut.x, 1.1, rel_tol=1e-7)
        assert math.isclose(sut.y, 2.5, rel_tol=1e-7)
        assert math.isclose(sut.z, 3.4, rel_tol=1e-7)

        assert sut.xy == Vec2(1.1, 2.5)
        assert sut.xz == Vec2(1.1, 3.4)

        assert sut.X == 1
        assert sut.Y == 2
        assert sut.Z == 3
        assert sut.XY == Vec2(1, 2)
        assert sut.XZ == Vec2(1, 3)

    def test_static_values(self):
        assert Vec3.zero == Vec3(0, 0, 0)
        assert Vec3.one == Vec3(1, 1, 1)
        assert Vec3.right == Vec3(1, 0, 0)
        assert Vec3.left == Vec3(-1, 0, 0)
        assert Vec3.up == Vec3(0, 1, 0)
        assert Vec3.down == Vec3(0, -1, 0)
        assert Vec3.forward == Vec3(0, 0, 1)
        assert Vec3.back == Vec3(0, 0, -1)