#-*- coding: utf-8 -*-
from PyQt4.QtCore import QCoreApplication

from mensageiroCore.servicos.servicoMensageiro import ServicoClienteMensageiro, ServicoServidorMensageiro
from utilTeste import printt


def teste(de, f):
    assert de == '127.0.0.1'
    assert f == "teste"
    print("OK")


app = QCoreApplication([])

b = ServicoServidorMensageiro()
a = ServicoClienteMensageiro()
a.setPara('127.0.0.1')
a.conversaRecebida.connect(teste)
b.listaClientesAtualizada.connect(printt)
b.dadosUsuarioAtualizado.connect(lambda u: print("ATUALIZADO:", u))

a.enviarConversa("teste")

app.exec_()
