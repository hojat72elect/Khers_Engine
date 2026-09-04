from ursina import Entity, Vec2, Vec3, color, distance, distance_2d, distance_xz, lerp, rotate_around_point_2d, make_gradient

class TestUrsinaMath:
    def test_general_behavior(self):

        sut1 = Entity(position=(0, 0, 0))
        sut2 = Entity(position=(0, 1, 1))
        assert distance(sut1, sut2) == 1.4142135623730951
        assert distance_2d(Vec2(0, 0), Vec2(1, 1)) == 1.4142135623730951
        assert distance_xz(sut1, sut2.position) == 1

        between_color = lerp(color.lime, color.magenta, 0.5)
        assert isinstance(between_color, color.Color)
        assert between_color == color.Color(0.75, 0.5, 0.5, 1.0)

        assert lerp((0, 0), (0, 1), 0.5) == (0, 0.5)
        assert lerp(Vec2(0, 0), Vec2(0, 1), 0.5) == Vec2(0, 0.5)
        assert lerp([0, 0], [0, 1], 0.5) == [0, 0.5]

        assert round(Vec3(0.38, 0.1351, 353.26), 2) == Vec3(0.38, 0.14, 353.26)

        point = (1, 0)
        assert rotate_around_point_2d(point, (0, 0), 90) == (6.123233995736766e-17, -1)

    def test_make_gradient(self):
        sut1 = make_gradient({'0':color.hex('#ff0000ff'), '2':color.hex('#ffffffff')})
        assert sut1 == [color.hex('#ff0000ff'), lerp(color.hex('#ff0000ff'), color.hex('#ffffffff'), 0.5),color.hex('#ffffffff')]

        sut2 = make_gradient({'0':color.hex('#ff0000ff'), '4':color.hex('#ffffffff')})
        assert sut2 == [
            color.hex("#ff0000ff"),
            lerp(color.hex("#ff0000ff"), color.hex("#ffffffff"), 0.25),
            lerp(color.hex("#ff0000ff"), color.hex("#ffffffff"), 0.5),
            lerp(color.hex("#ff0000ff"), color.hex("#ffffffff"), 0.75),
            color.hex("#ffffffff"),
        ]

        assert make_gradient({"0": 16, "2": 0}) == [16, 8, 0]
        assert make_gradient({"6": 0, "8": 8}) == [0, 4, 8]