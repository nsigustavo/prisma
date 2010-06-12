#!/usr/bin/env python
#-*- coding:utf-8 -*-
from diagramapic import PicSequencia, Raia
import os
import commands
import tempfile
import sys
import inspect
import traceback
from core import Sinal
from utils import normalizetipo


class DiagramaDeSequencia(object):
    """
    DiagramaDeSequencia: Criar um diagrama de sequencia apartir da execução de um código
    Exemplo:
        >>> with DiagramaDeSequencia(titulo="Diagrama de sequencia", src="caminho.svg", modulos=['Teste'])
        ...     t = Teste(actor=Gustavo)                                \ código  do
        ...     t.testando()                                            /  diagrama

Diagrama de sequencia                                 :Exemplo
         :                                                :
         :   Teste(actor=Gustavo)                         :
        | |--------------------->:                        :
        | |      «create»       | |                       :
        | |                     | |___inicializeTest()    :
        | |                     | |   |                   :
        | |                     || |<-Ꞌ                   :
        | |                     || |     getExample()     :
        | |                     || |--------------------->:
        | |     testando()       :                        :
        | |-------------------->| |                       :

    """

    def __init__(self, titulo, src, modulos, usuario=None, restringirPrivados=True):
        self._caminho = src
        self._titulo = titulo
        self._sequencia = PicSequencia(titulo)
        self._filtrar = Filtro(modulos=modulos, restringirPrivados=restringirPrivados)
        self._contextoInitical = self._contexto = ActorContext(titulo)
        self._traceAntigo = None

    def trace(self, frame, tipoDeChamada, retorno):
            if self._traceAntigo:
                self._traceAntigo(frame, tipoDeChamada, _)

            sinal = Sinal(frame)
            if self._filtrar(sinal):

                if tipoDeChamada == 'call':
                    self._contexto = self._contexto.menssagem(sinal)
                elif tipoDeChamada == "return" and retorno is not None:
                    self._contexto.feedback(retorno)

    def gravar(self):
        self._traceAntigo = sys.getprofile()
        sys.setprofile(self.trace)
        return self

    def __enter__(self):
        self.gravar()

    def __exit__(self, type, traceback, msg):
        self.parar()

    def parar(self):
        sys.setprofile(self._traceAntigo)
        self._contextoInitical.rederizar(self._sequencia)
        self._criarGrafico()

    def __repr__(self):
        return '<Diagrama de Sequencia: %s src(%s)>' %(self._titulo, self._caminho)

    def _criarGrafico(self):
        pic = self._sequencia.picDiagrama()
        pic2plot(pic, self._caminho)

def pic2plot(pic, caminho):
    tempDir = tempfile.mkdtemp()
    tempGraficoPic = os.path.join(tempDir, 'sequencia.pic')
    with file(tempGraficoPic, 'w') as grafico:
        grafico.write(pic)
    status, saida = commands.getstatusoutput("pic2plot -Tsvg %s > %s" %( tempGraficoPic, caminho))
    if status != 0:
        raise ReferenceError('Erro ao executar comando pic2plot:\n%s'%saida)          #Instalar: (sudo apt-get install plotutils)
    return saida


class Contexto(object):
    """Contexto em que metodos são chamados.
    | |___     Representa uma raia "ativa" na linha do tempo do diagrama de sequência.
    | |   |                :    desativa    |A|
    || |<-Ꞌ                :<- - - - - - - -|T|
    || |                   :                |I|
    || |    menssagem()    :                |V|
    || | ----------------> :                |A|
    """
    retorno = None
    def __init__(self, contextoAnterior, objetoChamado, profundidade=0, sinal=None):
        self.sinalDeContexto = sinal               #TODO: refatorar entrada do sinal
        self.profundidade = profundidade
        self.contextoAnterior = contextoAnterior
        self.objetoChamado = self._idObjetoChamado(objetoChamado)
        self.reprDoObjeto = self._reprDoObjeto(objetoChamado)
        self.chamadas = []

    def feedback(self, retorno):
        self.retorno = normalizetipo(retorno)

    def menssagem(self, sinal):
        if not sinal.ehmetodo():
            self.chamadas.append((sinal.menssagem(), self)) # Funcao chamada (adaptação para nao oo)
            return self
        novaProfundidade = sinal.profundidade()
        if novaProfundidade > self.profundidade:

            novoContexto = Contexto(
                            contextoAnterior=self,
                            objetoChamado=sinal.objetoChamado(),
                            profundidade=novaProfundidade,
                            sinal=sinal)
            self.chamadas.append((sinal.menssagem(), novoContexto))
            return novoContexto
        if novaProfundidade == self.profundidade:
            return self.contextoAnterior.menssagem(sinal)
        elif self.contextoAnterior and self.contextoAnterior.contextoAnterior:
            return self.contextoAnterior.contextoAnterior.menssagem(sinal)

    def rederizar(self, sequencia):
            sequencia.adicionarRaia(Raia(self.objetoChamado, self.reprDoObjeto))
            sequencia.ativar(self.objetoChamado)
            if self.chamadas:
                for chamada, novoContexto in self.chamadas:
                    created = chamada.startswith("__init__")
                    sequencia.adicionarRaia(Raia(novoContexto.objetoChamado, novoContexto.reprDoObjeto, created))
                    if created:
                        sequencia.menssagemDeCriacao(
                            self.objetoChamado,
                            novoContexto.objetoChamado,
                            novoContexto.sinalDeContexto.menssagemDeCriacao(),
                            )
                    else:
                        sequencia.menssagem(self.objetoChamado, novoContexto.objetoChamado, chamada)
                    if not novoContexto is self :
                        novoContexto.rederizar(sequencia)
            if self.retorno:
                sequencia.menssagemDeRetorno(self.objetoChamado, self.contextoAnterior.objetoChamado, self.retorno)
            sequencia.desativar(self.objetoChamado)

    def _reprDoObjeto(self, ob):
        return normalizetipo(ob)

    def _idObjetoChamado(self, objeto):
        """
        Id do objeto chamado
            - o id é composto por Letras em caixa alta por limitação do pic
        """
        uid =  str(id(objeto))
        for numero, letra in enumerate("ABCDEFGHIJ"):
            uid = uid.replace(str(numero), letra)
        return uid


class ActorContext(Contexto):
    """Contexto inicial representando a ação de um ator
       __0__
         |
        / \
Gustavo:Desenvolvedor      Exemplo
        |A|                   :
        |C|    menssagem()    :
        |T|------------------>:
        |O|                   :
        |R|                   :
    """
    def __init__(self, descricao):
        self.profundidade = 0
        self.contextoAnterior = None
        self.reprDoObjeto = descricao
        self.objetoChamado = "Actor"
        self.chamadas = []


class Filtro(object):
    def __init__(self, modulos=[], restringirPrivados=False):
        self._modulos = modulos
        self.restringirPrivados = restringirPrivados

    def validar(self, sinal):
        return  self.modulos(sinal) and self.metodos(sinal) and self.privados(sinal)

    def modulos(self, sinal):
        return sinal.estaContidoEm(self._modulos)

    def metodos(self, sinal):
        try:
            return sinal.ehmetodo()
        except:
            return True

    def privados(self, sinal):
        metodoName = sinal.metodoChamado()
        return not ((metodoName.startswith("_")
                   and not metodoName.endswith("__")
                   or  metodoName in ['__nonzero__'])
               and self.restringirPrivados)

    def __call__(self, frame):
        return self.validar(frame)

