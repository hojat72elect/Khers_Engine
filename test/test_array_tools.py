from ursina import Array2D, sample_bilinear, list_2d_to_string, string_to_2d_list, rotate_2d_list
from textwrap import dedent, indent

class TestArrayTools:
    def test_general_behavior(self):
        sut = Array2D(data=[
            [1, 1, 0],
            [1, 0, 0],
            [1, 0, 0],
        ])

        assert sample_bilinear(sut, 0, 0) == 1
        assert sample_bilinear(sut, 1, 1) == 0
        assert sample_bilinear(sut, 0.5, 0.5) == 0.75
        assert sample_bilinear(sut, 0.5, 0.75) == 0.625

    def test_list_to_string(self):
        sut = [
            [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
            [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
            [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],
        ]
        expected_result = dedent("""
                #..#.###..####..#..
                #..#.#..#.###...#..
                #..#.###.....#..#..
                .##..#..#.####..#..
                """).strip()

        assert list_2d_to_string(sut) == expected_result

    def test_rotate_2d_list(self):
        assert string_to_2d_list("""\
        #..#.###..####..#..
        #..#.#..#.###...#..
        #..#.###.....#..#..
        .##..#..#.####..#..
        """) == rotate_2d_list([
                [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],
                [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0],
                [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                [0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],
            ])
        
    def test_array_from_string(self):
        sut = Array2D(width=16, height=8)
        sut.add_margin(top=4, right=7, bottom=3, left=2, value=7)

        assert Array2D(data=[[1, 6], [2, 7], [3, 8], [4, 9], [5, 10]]).to_string() == indent(
            dedent("""
                6,  7,  8,  9, 10
                1,  2,  3,  4,  5
                """).strip(),
            " ",
        )
        
        assert Array2D(data=[[1,6], [2,7], [3,8], [4,9], [5,10]]).rows == [[1,2,3,4,5], [6,7,8,9,10]]
        assert Array2D.from_string(
            """
        0,1,0
        2,3,4
        0,1,1
        0,0,0
        """,
            int,
        ) == Array2D(data=[
                                [0, 0, 2, 0],
                                [0, 1, 3, 1],
                                [0, 1, 4, 0]
        ])
    
