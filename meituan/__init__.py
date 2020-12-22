from time import time, sleep


def get_parameter(a, b, **kwargs):
    def retryerrror(func):
        print(a, b)
        def wrapper(*args, **kwargs):
            print(args, kwargs)
            try:
                print(time())
                result = func(*args, **kwargs)
                print(time())
            except Exception as e:
                err_text = f'重试n次失败报错 {e} '
                print(err_text)
                return False
            return result

        return wrapper
    return retryerrror


@get_parameter(a=1, b=2, c=5)
def aa(a, b):
    print(a, b, "aa")
    sleep(2)
    print("this is aa")


aa(a=3, b=4)
