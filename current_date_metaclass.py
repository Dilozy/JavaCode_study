from datetime import datetime


class MetaDateTime(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=MetaDateTime):
    pass

my_class = MyClass()
print(my_class.created_at)