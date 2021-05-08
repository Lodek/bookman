from functools import reduce

def compose(fs):
    """
    Returns function that is a composition of `fs`.
    It's up to the user to ensure these functions can be chained.
    """
    def composition(*args, **kwargs):
        funcs = list(fs)
        f = funcs.pop(0)
        result = f(*args, **kwargs)
        for f in funcs:
            result = f(result)
        return result
    return composition

def pascal_to_kebab(string):
    mapper = lambda char: char if char.islower() else "-" + char
    kebabed = reduce(lambda acc, char: acc + mapper(char), string)
    return kebabed.lower().strip('-')
