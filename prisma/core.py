#!/usr/bin/env python
#-*- coding:utf-8 -*-


import inspect
from utils import caminho, normalizetipo


class Sinal(object):

    def __init__(self, frame):
        self._frame = frame

    def profundidade(self):
        frame = self._frame
        n=0
        while frame is not None:
            n+=1
            frame = frame.f_back
        return n

    def caminho(self, obj=None):
        return caminho(obj or self._frame)

    def __repr__(self):
        return self.metodoChamado() + ': Sinal'

    def estaContidoEm(self, modulos):
        return any([ self.caminho(modulo) in self.caminho()
            for modulo in modulos])

    def metodoChamado(self):
        escopo = inspect.getframeinfo(self._frame).function
        if escopo == '<module>':
            return self._frame.f_code.co_filename
        else:
            return escopo

    def _normalizetipo(self, objeto):
        return normalizetipo(objeto)

    def filename(self, frame=None):
        frame = frame or self._frame
        return frame.f_code.co_filename

    def menssagem(self):
        return self.metodoChamado() + self._parametros()

    def menssagemDeCriacao(self):
        if self.metodoChamado() == "__init__":
            return self.objetoChamado().__class__.__name__ + self._parametros()

    def _variaveisLocais(self):
        if self.objetoChamado() is self._frame:
            return self._locals().items()
        defaults = self._parametrosDefaults()
        parametros = self._nomeDosParametros()
        variaveis =  self._locals()
        variaveisLocais = []
        for posicao, parametro in enumerate(parametros, 1):
            if len(defaults) > (len(parametros) - posicao):
                if not defaults[-((len(parametros) - posicao) + 1)] == variaveis.get(parametro):
                    variaveisLocais.append((parametro, variaveis.get(parametro)))
            else:
                variaveisLocais.append((parametro,  variaveis.get(parametro, None)))
        return variaveisLocais

    def _locals(self):
        return self._frame.f_locals

    def _parametrosDefaults(self):
        objetoChamado = self.objetoChamado()
        metodo = getattr(objetoChamado, self.metodoChamado())
        return metodo.im_func.func_defaults or []

    def _nomeDosParametros(self):
        argcount = self._frame.f_code.co_argcount
        if argcount:
            parametros = list(self._frame.f_code.co_varnames)[:argcount]
            if 'self' in parametros: parametros.remove('self')
            if 'cls' in parametros: parametros.remove('cls')
            return parametros
        return []

    def _parametros(self):
        return "("+",".join(['%s=%s'%(name, self._normalizetipo(valor))
            for name, valor in self._variaveisLocais()])+')'

    def ehmetodo(self):
        return any([self._locals().get(nomeDoObjeto, None) for nomeDoObjeto in ('self', "cls")])

    def objetoChamado(self):
        return self._locals().get('self') or self._locals().get('cls') or self._frame

