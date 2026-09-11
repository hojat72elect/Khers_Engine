from ursina.scripts.property_generator import generate_properties_for_class

if __name__ == "__main__":

    class Z:
        pass

    @generate_properties_for_class(getter_suffix="_getter", setter_suffix="_setter")
    class A:
        pass

    @generate_properties_for_class()
    class B(A):
        def __init__(self):
            super().__init__()

        def x_setter(self, value):
            self._x = value

            print("B setter side effect")

    e = B()
    e.x = 2
    print("xxxxxxxx", e.x)
