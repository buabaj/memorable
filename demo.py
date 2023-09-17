from memorable.core import Memorable


@Memorable()
def sample_func():
    # Allocate objects and potentially create memory leaks
    big_list = [0] * 1000000
    # ...

if __name__ == "__main__":
    sample_func()
