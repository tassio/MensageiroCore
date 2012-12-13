#-*- coding: utf-8 -*-

from PyQt4.QtCore import pyqtSignal
from mensageiroCore.servicos.informacao.informacaoMensageiro import Usuario
from networkService.servicos.servicoConexao import ServicoConexaoCliente, \
    ServicoConexaoServidor
from networkService.servicos.servicoConversa import ServicoConversaCliente, \
    ServicoConversaServidor
from mensageiroCore.servicos import conf



class _ServicoMensageiro:
    DADOS_USUARIO = 30
    LISTA_USUARIOS = 31
    PEDIR_DADOS = 32
    USUARIO_ALTERADO = 33


class ServicoClienteMensageiro(ServicoConversaCliente):
    listaClientesAtualizada = pyqtSignal(list)
    dadosUsuarioAtualizado = pyqtSignal(Usuario)
    conectado = pyqtSignal(bool)
    def __init__(self, portaReceber=45455, portaResponder=45456, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, ipServidor=conf.IP_SERVIDOR, parent=parent)
        
        self._servicoConexao = ServicoConexaoCliente(self)
        self._servicoConexao.conectadoServidor.connect(self._emitirConectadoEAtualizarUsuarios)

        self._usuarioAtual = Usuario()
        self._usuarioAtual.load()

        self._enviarInformacaoUsuario()

    def _receberInformacaoTipoValor(self, de, tipo, valor):
        if tipo == _ServicoMensageiro.LISTA_USUARIOS:
            self.listaClientesAtualizada.emit(valor)
        elif tipo == _ServicoMensageiro.USUARIO_ALTERADO:
            self.dadosUsuarioAtualizado.emit(valor.copy())
        elif tipo == _ServicoMensageiro.PEDIR_DADOS:
            self._enviarInformacaoUsuario()

        super()._receberInformacaoTipoValor(de, tipo, valor)

    def _emitirConectadoEAtualizarUsuarios(self, con):
        self.conectado.emit(con)
        if con:
            self.atualizarDadosUsuarios()

    def atualizarDadosUsuarios(self):
        self._enviarInformacaoServidor(_ServicoMensageiro.PEDIR_DADOS)

    def estaConectado(self):
        return self._servicoConexao.estaConectado()

    def _enviarInformacaoUsuario(self):
        if self._servicoConexao.estaConectado():
            self._enviarInformacaoServidor(_ServicoMensageiro.DADOS_USUARIO, self._usuarioAtual)

    def setNome(self, nome):
        if nome != self.getNome():
            self._usuarioAtual.setNome(nome)
            self._usuarioAtual.save()
            self._enviarInformacaoUsuario()

    def getNome(self):
        return self._usuarioAtual.getNome()

    def setStatus(self, status):
        if status != self.getStatus():
            self._usuarioAtual.setStatus(status)
            self._usuarioAtual.save()
            self._enviarInformacaoUsuario()

    def getStatus(self):
        return self._usuarioAtual.getStatus()
        

class ServicoServidorMensageiro(ServicoConversaServidor):
    listaClientesAtualizada = pyqtSignal(list)
    dadosUsuarioAtualizado = pyqtSignal(Usuario)
    def __init__(self, portaReceber=45456, portaResponder=45455, parent=None):
        super().__init__(portaReceber=portaReceber, portaResponder=portaResponder, parent=parent)

        self._servicoConexao = ServicoConexaoServidor(self)
        self._servicoConexao.listaIPsClientesAtualizada.connect(self._pedirDadosUsuarios)
        self._dadosUsuarios = {}

    def _receberInformacaoTipoValor(self, de, tipo, valor):
        if tipo == _ServicoMensageiro.DADOS_USUARIO:
            usuario = valor.copy()
            usuario.setIP(de)

            self._dadosUsuarios[de] = usuario
            
            self._enviarDadosUsuario(usuario)
            self.dadosUsuarioAtualizado.emit(usuario)
            self.listaClientesAtualizada.emit(self.getDadosUsuarios())
        elif tipo == _ServicoMensageiro.PEDIR_DADOS:
            for usuario in self.getDadosUsuarios():
                self.enviarInformacaoTipoValor(_ServicoMensageiro.USUARIO_ALTERADO, usuario, de)
        
        super()._receberInformacaoTipoValor(de, tipo, valor)

    def _enviarDadosUsuario(self, usuario):
        self._enviarInformacaoParaClientes(_ServicoMensageiro.USUARIO_ALTERADO, usuario)

    def _pedirDadosUsuarios(self):
        self._enviarInformacaoParaClientes(_ServicoMensageiro.PEDIR_DADOS, None)
            
    def _enviarInformacaoParaClientes(self, tipo, valor):
        for ip in self._servicoConexao.listaIPsClientes():
            self.enviarInformacaoTipoValor(tipo, valor, ip)

    def _atualizarListaIPsClientes(self):
        self._servicoConexao.atualizarListaIPsClientes()

    def getDadosUsuarios(self):
        return list(self._dadosUsuarios.values())

    def atualizarListaClientes(self):
        self._atualizarListaIPsClientes()
        self._pedirDadosUsuarios()
        