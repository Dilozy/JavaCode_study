import functools


class UserRoleContext:
    def __init__(self, roles):
        self.roles = roles

    def __enter__(self):
        return self.roles

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def acess_control(roles=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if set(user_roles) & set(roles):
                return func(*args, **kwargs)
            
            raise PermissionError("У вас недостаточно прав для выполнения данного действия")

        return wrapper
    return decorator


@acess_control(roles=["admin", "moderator"])
def sum_nums(a, b):
    return a + b


try:
    with UserRoleContext(["admin", "moderator"]) as user_roles:
        print(sum_nums(5, 2))
except PermissionError as exc:
    print(f"Ошибка: {exc}")
