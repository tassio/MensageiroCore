#-*- coding: utf-8 -*-
from PyQt4.QtCore import Qt

from networkService.servicos.informacao import InformacaoAbstrata, DataManipulador, RegistroInformacao
from mensageiroCore.servicos import conf


class Status:
    OFFLINE = 0
    ONLINE = 1
    OCUPADO = 2
    AUSENTE = 3
    STATUS = ["OFFLINE", "ONLINE", "OCUPADO", "AUSENTE"]
    def __init__(self, ind=0):
        if not 0 <= ind < len(Status.STATUS):
            raise IndexError("Nao existe esse status, informe um indice entre 0 e {0}".format(len(Status.STATUS) - 1))

        self._ind = ind
        
    def __eq__(self, st):
        if isinstance(st, Status):
            return st.getIndice() == self.getIndice()
        elif isinstance(st, int):
            return st == self.getIndice()
        elif isinstance(st, str):
            return st == str(self)
        
        return False
        
    def __str__(self):
        return Status.STATUS[self._ind]

    def getIndice(self):
        return self._ind

    def corStatus(self):
        return [Qt.black, Qt.green, Qt.red, Qt.yellow][self._ind]
    
    @staticmethod
    def getInstance(nome):
        return Status(Status.STATUS.index(nome))


@RegistroInformacao.addInformacaoHandler(Status)
class InformacaoStatus(InformacaoAbstrata):
    def __rshift__(self, data):
        DataManipulador(data).addInstance(self.valor.getIndice())

    def __lshift__(self, data):
        self.valor = Status(DataManipulador(data).getNextInstance())


class Usuario(object):
    def __init__(self, nome="", status=Status(Status.OFFLINE), ip=""):
        self.nome = nome
        self.status = status
        self.ip = ip

    def setNome(self, nome):
        self.nome = nome
    def getNome(self):
        return self.nome

    def setStatus(self, status):
        self.status = status
    def getStatus(self):
        return self.status

    def setIP(self, ip):
        self.ip = ip
    def getIP(self):
        return self.ip

    def __eq__(self, us):
        return us != None and \
               us.nome == self.nome and \
               us.status == self.status and \
               us.ip == self.ip

    def __str__(self):
        return "NOME: {0.nome} - STATUS: {0.status} - IP: {0.ip}".format(self)

    def save(self):
        #Salvar no arquivo de configuracao
        #with open("../conf/conf.dat", 'w') as arq:
        #    arq.write(self.nome + "<!>" + str(self.status))
        pass

    def load(self):
        #Carregar do arquivo de configuracao
        #with open("../conf/conf.dat", 'r') as arq:
        #    self.nome, st = arq.readline().split("<!>")
        #    self.status = Status(Status.STATUS.index(st))
        self.nome = conf.NOME_USUARIO_PADRAO
        self.status = Status.getInstance(conf.STATUS_PADRAO)

    def copy(self):
        return Usuario(self.nome, self.status, self.ip)

    
@RegistroInformacao.addInformacaoHandler(Usuario)
class InformacaoUsuario(InformacaoAbstrata):
    def __lshift__(self, data):
        dataLeitura = DataManipulador(data)
        
        self.valor = Usuario()
        self.valor.setNome(dataLeitura.getNextInstance())
        self.valor.setStatus(dataLeitura.getNextInstance())
        self.valor.setIP(dataLeitura.getNextInstance())

    def __rshift__(self, data):
        dataEscrita = DataManipulador(data)
        
        dataEscrita.addInstance(self.valor.getNome())
        dataEscrita.addInstance(self.valor.getStatus())
        dataEscrita.addInstance(self.valor.getIP())

