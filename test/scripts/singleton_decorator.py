from ursina.scripts.singleton_decorator import singleton

if __name__ == '__main__':

    class MyBaseClass:
        def __init__(self, name):
            self.name = name

    @singleton
    class DecoratedClass(MyBaseClass):
        def __init__(self, name='decorated_class'):
            super().__init__(name)

    app = DecoratedClass()
    app_2 = DecoratedClass()
    from ursina.ursinastuff import _test
    _test(app == app_2)
