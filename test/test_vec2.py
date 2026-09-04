from ursina import Vec2


class TestVec2:
    def test_general_behavior(self):
        sut = Vec2(1, 1)
        assert sut.X == 1
        assert sut.Y == 1
        assert sut.XY == (1, 1)

        sut.x = 3
        sut.y = 3
        assert sut.X == 3
        assert sut.Y == 3
        assert sut.XY == (3, 3)

    def test_rounding_a_vec2(self):
        aVector = Vec2(3.9, 5.2)
        sut = round(aVector)

        assert sut.X == 3
        assert sut.Y == 5

    def test_vec2_constants(self):
        assert Vec2.zero == Vec2(0, 0)
        assert Vec2.one == Vec2(1, 1)
        assert Vec2.right == Vec2(1, 0)
        assert Vec2.left == Vec2(-1, 0)
        assert Vec2.up == Vec2(0, 1)
        assert Vec2.down == Vec2(0, -1)

        assert Vec2.cardinal_directions == (Vec2.up, Vec2.right, Vec2.down, Vec2.left)
        assert Vec2.ordinal_directions == (
            Vec2(1, 1),
            Vec2(1, -1),
            Vec2(-1, -1),
            Vec2(-1, 1),
        )
        assert (
            Vec2.compass_directions
            == Vec2.cardinal_directions + Vec2.ordinal_directions
        )
