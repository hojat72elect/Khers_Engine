from types import FunctionType

def generate_properties_for_class(getter_suffix='_getter', setter_suffix='_setter', deleter_suffix='_deleter'):
    def decorator(cls):
        names = set()
        getters = {}
        setters = {}
        deleters = {}

        # local_methods = dir(cls)
        local_methods = {x:y for x, y in cls.__dict__.items() if isinstance(y, FunctionType | classmethod | staticmethod)}
        for name in local_methods:
            if name.endswith(getter_suffix):
                base_name = name[:-len(getter_suffix)]
                getters[base_name] = getattr(cls, name)
                names.add(base_name)

            if name.endswith(setter_suffix):
                base_name = name[:-len(setter_suffix)]
                setters[base_name] = getattr(cls, name)
                names.add(base_name)

            if name.endswith(deleter_suffix):
                base_name = name[:-len(deleter_suffix)]
                deleters[name[:-len(deleter_suffix)]] = getattr(cls, name)
                names.add(base_name)


        for name in names:
            getter = getters.get(name, None)
            setter = setters.get(name, None)
            deleter = deleters.get(name, None)

            if not getter:
                # print('make default getter for', cls, name, f'_{name}')
                def default_getter(cls, name=name):
                    return getattr(cls, f'_{name}', None)
                getter = default_getter

            if not setter:
                def default_setter(cls, value, name=name):
                    setattr(cls, f'_{name}', value)
                setter = default_setter

            if not deleter:
                def default_deleter(cls, name=name):
                    delattr(cls, f'_{name}')
                deleter = default_deleter

            setattr(cls, name, property(getter, setter, deleter))

        return cls
    return decorator
