from functools import reduce

def compose(fs):
    """
    Returns function that is a composition of `fs`.
    It's up to the user to ensure these functions can be chained.
    """
    def composition(*args, **kwargs):
        f = fs.pop(0)
        result = f(*args, **kwargs)
        for f in fs:
            result = f(result)
        return result
    return composition
