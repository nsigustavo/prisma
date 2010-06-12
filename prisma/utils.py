from contextlib import contextmanager
from sys import _getframe
import inspect
import os
import sys

Frame = type(_getframe(1))

camimnhoDoPython = os.path.dirname(inspect.getsourcefile(os))


def caminho(modulo):
    if isinstance(modulo, str):
        return modulo
    elif isinstance(modulo, Frame):
        return os.path.splitext(modulo.f_code.co_filename)[0]
    else:
        arquivoDoCodigo = inspect.getsourcefile(modulo)
        if os.path.dirname(arquivoDoCodigo or '') == camimnhoDoPython:
            return os.path.splitext(arquivoDoCodigo)[0]
        else:
            return os.path.dirname(arquivoDoCodigo or '') or '<doctest>'


def normalizetipo(objetoChamado):
    if type(objetoChamado) is Frame:
        return "Func:"+ objetoChamado.f_code.co_name
    if type(objetoChamado) is type:
        return objetoChamado.__name__
    if isinstance(objetoChamado, (int, float, bool)):
        return str(objetoChamado)
    if isinstance(objetoChamado, tuple):
        return "(%s)"%", ".join(["%s"%normalizetipo(item) for item in objetoChamado])
    if isinstance(objetoChamado, list):
        return "[%s]"%", ".join(["%s"%normalizetipo(item) for item in objetoChamado])
    if isinstance(objetoChamado, dict):
        return "{%s}"%", ".join(["%s:%s"%(normalizetipo(key), normalizetipo(value)) for key, value in objetoChamado.items()])
    if objetoChamado is None:
        return 'None'
    if isinstance(objetoChamado, (str)):
        return "%r"%objetoChamado[:30]

    if hasattr(objetoChamado, '__repr__') and not objetoChamado.__repr__ == object.__repr__:
        return str(repr(objetoChamado)).replace('"',"'")

    return "%s: %0.40s"% (objetoChamado.__class__.__name__,  ", ".join(['%s=%0.30r'%(attr, normalizetipo(getattr(objetoChamado, attr)))
        for attr in dir(objetoChamado)
            if type(getattr(objetoChamado, attr)) in (str, int, float, bool)
            and not attr.startswith('_')]))


@contextmanager
def stdout_redirected(new_stdout):
    save_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield None
    finally:
        sys.stdout = save_stdout

