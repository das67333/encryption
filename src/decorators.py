import functools
import time
def timing(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()
        print('Time taken:', te - ts, 'sec')
        return result
    return wrapper
