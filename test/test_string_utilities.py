from ursina import camel_to_snake, snake_to_camel


class TestStringUtilities:
    def test_general_behavior(self):
        assert camel_to_snake("CamelToSnake") == "camel_to_snake"
        assert snake_to_camel("snake_to_camel") == "SnakeToCamel"
