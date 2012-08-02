import inspect

def getRequiredArgs(func):
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if defaults:
        args = args[:-len(defaults)]
    return args   # *args and **kwargs are not required, so ignore them.
    
def missingArgs(func, argdict):
    return set(getRequiredArgs(func)).difference(argdict)
    
def invalidArgs(func, argdict):
    args, varargs, varkw, defaults = inspect.getargspec(func)
    if varkw: return set()  # All accepted
    return set(argdict) - set(args)

def isCallableWithArgs(func, argdict):
    return not missingArgs(func, argdict) and not invalidArgs(func, argdict)