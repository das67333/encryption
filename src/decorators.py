import functools, time, tkinter


def messagebox(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exception:
            tkinter.messagebox.showerror('', exception)

    return inner


def duration(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        ts = time.time()
        func(*args, **kwargs)
        te = time.time()
        return te - ts

    return inner
