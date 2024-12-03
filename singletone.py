from singletone_instance import singletone_import


class SingletoneNew:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


first = SingletoneNew()
second = SingletoneNew()
print(first is second)


class Meta(type):
    _instance = None
    
    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class SingletoneMeta(metaclass=Meta):
    pass


third = SingletoneMeta()
fourth = SingletoneMeta()
print(third is fourth)

# Синглтон через механизм импорта

print(singletone_import.value)
singletone_import.value = True

from singletone_instance import singletone_import 

print(singletone_import.value)