from StringIO import StringIO
from utils import caminho, stdout_redirected


class PicSequencia:
    def __init__(self, titulo):
        self.titulo = titulo
        self._raias = []
        self._sequencia = []

    def picDiagrama(self):
        saida = StringIO()
        with stdout_redirected(saida):
            print '.PS'
            print 'copy "%s";'% (caminho(PicSequencia) + '/sequencia.pic')
            print 'boxwid = 0;'
            print 'boxht = 0;'
            print 'underline = 0;'
            print 'spacing = 0.6;'

            for raia in self._raias:
                print "placeholder_object(%sDummy);"%raia.objetoId() # mais espaco
                print "placeholder_object(%sDummyy);"%raia.objetoId() # mais espaco
                print "placeholder_object(%sDummyyy);"%raia.objetoId() # mais espaco
                print raia.inicializeRaia()
            print 'step();'

            for passo in self._sequencia:
                print str(passo)

            for raia in self._raias:
                print 'complete(%s);' %(raia.objetoId())

            print '.PE',
        return saida.getvalue()

    def ativar(self, objetoId):
        if not objetoId in  self._objetoIds():
            raise AttributeError("Objeto '%s' tem que ser adicionado"%objetoId)
        self._sequencia.append(Ativar(objetoId))

    def _objetoIds(self):
        return [raias.objetoId() for raias in self._raias]

    def menssagem(self, transmissorId, receptorId, msg):
        if not transmissorId in  self._objetoIds():
            raise AttributeError("Objeto '%s' tem que ser adicionado"%transmissorId)
        if not receptorId in  self._objetoIds():
            raise AttributeError("Objeto '%s' tem que ser adicionado"%receptorId)
        self._sequencia.append(Menssagem(transmissorId, receptorId, msg))

    def menssagemDeCriacao(self, transmissorId, receptorId, representacao):
        self._sequencia.append(MenssagemDeCriacao(transmissorId, receptorId, representacao))

    def desativar(self, objetoId):
        self._sequencia.append(Desativar(objetoId))

    def adicionarRaia(self, raia):
        if not raia.objetoId() in self._objetoIds():
            self._raias.append(raia)

    def menssagemDeRetorno(self, transmissorId, receptorId, resposta):
        self._sequencia.append(MenssagemDeRetorno(transmissorId, receptorId, resposta))

    def __repr__(self):
        return "<PicSequencia: %s>" % self.titulo

class Raia(object):

    def __init__(self, objetoId, descricao, reserva=False):
        self._objetoId = objetoId
        self._descricao = descricao.replace('"',"'")
        self._somenteReserve = reserva

    def objetoId(self):
        return self._objetoId

    def inicializeRaia(self):
        if self._objetoId is "Actor":
            return  'actor(%s,"%s");' %(self._objetoId, self._descricao)
        if self._somenteReserve:
            return "placeholder_object(%s);"%(self._objetoId)
        return 'object(%s,"%s");' %(self._objetoId, self._descricao)

    __repr__ = inicializeRaia

    def __eq__(self, raia):
        return bool(isinstance(raia, Raia) and raia.objetoId == self._objetoId)


class MenssagemDeCriacao(object):

    def __init__(self, transmissorId, objetoCriadoId, representacao):
        self.transmissorId = transmissorId
        self.objetoCriadoId = objetoCriadoId
        self.representacao = representacao

    def __str__(self):
        return 'create_message(%s,%s,"%s");'% (self.transmissorId, self.objetoCriadoId, self.representacao)
    __repr__ = __str__


class Ativar(object):

    def __init__(self, objeto):
        self.objeto = objeto

    def __str__(self):
        return "active(%s);"% self.objeto
    __repr__ = __str__


class Menssagem(object):

    def __init__(self, transmissorId, receptorId, msg):
        self.transmissorId = transmissorId
        self.receptorId = receptorId
        self.msg = msg

    def __str__(self):
        return 'message(%s,%s,"%s");'% (self.transmissorId, self.receptorId, self.msg)
    __repr__ = __str__


class Desativar(object):

    def __init__(self, objeto):
        self.objeto = objeto

    def __str__(self):
        return "inactive(%s);"% self.objeto
    __repr__ = __str__

class MenssagemDeRetorno(Menssagem):
    def __str__(self):
        return 'rmessage(%s,%s,"%s");'% (self.transmissorId, self.receptorId, self.msg)

