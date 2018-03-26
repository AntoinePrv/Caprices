# coding: utf-8


import functools
import inspect

# This is our decorator, it's a function that takes original
# function (func) and return a modified function (wrapper)
def apply_type(func):
    # This decorator let us transpose the meta information
    # of func on our new function wrapper
    @functools.wraps(func)
    # This is the new function we're creating. It takes
    # whatever we give it (*args, **kwargs)
    def wrapper(*args, **kwargs):
        # We inspect the signature of func
        sig = inspect.signature(func)
        # This let us get a parameter name for every argument
        # even if it's apply positionally. It's the resolution
        # Python does.
        bind = sig.bind(*args, **kwargs)
        # Looping through all arguements name and value
        for name, val in bind.arguments.items():
            # We get the annotation (the type hint)
            ann = sig.parameters[name].annotation
            # If there is a type hint
            if ann is not inspect._empty:
                # Then we apply the type hint to the input
                bind.arguments[name] = ann(val)
        # We apply the original function with the modified
        # arguments
        return func(*bind.args, **bind.kwargs)
    # We return the modified function
    return wrapper