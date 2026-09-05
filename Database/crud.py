from sqlalchemy.orm import Session
from database import Conta, Categorias, Investimentos, Transacoes,Cartoes , Faturas
from database import _Sessao
from datetime import datetime

# CONTAS #

def criar_conta(nome, tipo, saldo=0):
    db = _Sessao()

    try:
        conta = Conta(nome=nome, tipo=tipo, saldo=saldo, data_criação=datetime.now())
        db.add(conta)
        db.commit()
        db.refresh(conta)

    finally:
        db.close()

    return conta

def listar_contas():
    db = _Sessao()
    try:
        contas = db.query(Conta).all()
    finally:
        db.close()

def buscar_conta(conta_id):
    db = _Sessao()
    try:
        conta = db.query(Conta).filter(Conta.id == conta_id).first()
    finally:
        db.close()

def atualizar_conta(id, nome=None, tipo=None, saldo=None):
    db = _Sessao()
    try:
        conta = db.query(Conta).filter(Conta.id == id).first()
        if conta is None:
            return None
        if nome is not None:
            conta.nome = nome
        if tipo is not None:
            conta.tipo = tipo
        if saldo is not None:
            conta.saldo = saldo

        db.commit()
        db.refresh(conta)
        return conta
    finally:
        db.close()


def excluir_conta(id):
    db = _Sessao()
    try:
        conta = db.query(Conta).filter(Conta.id == id).first()
        if conta is None:
            return False

        db.delete(conta)
        db.commit()

        return True
    finally:
        db.close()



# cartoes #

def criar_cartao(conta_id,categoria_id,descricao,valor,tipo,parcelas,data):
    db = _Sessao()

    try:
        cartao = Cartoes(conta_id=conta_id,categoria_id=categoria_id,descricao=descricao,valor=valor,tipo=tipo,parcelas=parcelas,data=data)
        db.add(cartao)
        db.commit()
        db.refresh(cartao)

    finally:
        db.close()

    return cartao

def listar_cartoes():
    db = _Sessao()
    try:
        cartoes = db.query(Cartoes).all()
    finally:
        db.close()


def buscar_cartao(cartao_id):
    db = _Sessao()
    try:
        cartao = db.query(Cartoes).filter(Cartoes.id == cartao_id).first()
    finally:
        db.close()

def atualizar_cartao(id, conta_id=None,categoria_id=None,descricao=None,valor=None,tipo=None,parcelas=None,data=None):
    db = _Sessao()
    try:
        cartao = db.query(Cartoes).filter(Cartoes.id == id).first()
        if cartao is None:
            return None
        if conta_id is not None:
            cartao.conta_id = conta_id
        if categoria_id is not None:
            cartao.categoria_id = categoria_id
        if descricao is not None:
            cartao.descricao = descricao
        if valor is not None:
            cartao.valor = valor
        if tipo is not None:
            cartao.tipo = tipo
        if parcelas is not None:
            cartao.parcelas = parcelas
        if data is not None:
            cartao.data = data

        db.commit()
        db.refresh(cartao)
        return cartao
    finally:
        db.close()

def excluir_cartao(id):
    db = _Sessao()
    try:
        cartao = db.query(Cartoes).filter(Cartoes.id == id).first()
        if cartao is None:
            return False

        db.delete(cartao)
        db.commit()

        return True
    finally:
        db.close()

# Categorias #

def criar_categoria(nome, tipo):
    db = _Sessao()

    try:
        categoria = Categorias(nome=nome, tipo=tipo)
        db.add(categoria)
        db.commit()
        db.refresh(categoria)

    finally:
        db.close()

    return categoria

def listar_categorias():
    db = _Sessao()
    try:
        categorias = db.query(Categorias).all()
    finally:
        db.close()

def buscar_categoria(categoria_id):
    db = _Sessao()
    try:
        categoria = db.query(Categorias).filter(Categorias.id == categoria_id).first()
    finally:
        db.close()
    return categoria

def atualizar_categoria(id, nome=None, tipo=None):
    db = _Sessao()
    try:
        categoria = db.query(Categorias).filter(Categorias.id == id).first()
        if categoria is None:
            return None
        if nome is not None:
            categoria.nome = nome
        if tipo is not None:
            categoria.tipo = tipo

        db.commit()
        db.refresh(categoria)
        return categoria
    finally:
        db.close()

def excluir_categoria(id):
    db = _Sessao()
    try:
        categoria = db.query(Categorias).filter(Categorias.id == id).first()
        if categoria is None:
            return False

        db.delete(categoria)
        db.commit()

        return True
    finally:
        db.close()

# Faturas #

def criar_fatura(cartao_id,Mês,ano,Valor,data_vencimento,Status):
    db = _Sessao()

    try:
        fatura = Faturas(cartao_id=cartao_id,Mês=Mês,Ano=ano,Valor=Valor,data_vencimento=data_vencimento,Status=Status)
        db.add(fatura)
        db.commit()
        db.refresh(fatura)

    finally:
        db.close()


    return fatura

def listar_faturas():
    db = _Sessao()
    try:
        faturas = db.query(Faturas).all()
    finally:
        db.close()

def buscar_fatura(fatura_id):
    db = _Sessao()
    try:
        fatura = db.query(Faturas).filter(Faturas.id == fatura_id).first()
    finally:
        db.close()
    return fatura

def atualizar_fatura(id, cartao_id=None,Mês=None,ano=None,Valor=None,data_vencimento=None,Status=None):
    db = _Sessao()
    try:
        fatura = db.query(Faturas).filter(Faturas.id == id).first()
        if fatura is None:
            return None
        if cartao_id is not None:
            fatura.cartao_id = cartao_id
        if Mês is not None:
            fatura.Mês = Mês
        if ano is not None:
            fatura.Ano = ano
        if Valor is not None:
            fatura.Valor = Valor
        if data_vencimento is not None:
            fatura.data_vencimento = data_vencimento
        if Status is not None:
            fatura.Status = Status

        db.commit()
        db.refresh(fatura)
        return fatura
    finally:
        db.close()

def excluir_fatura(id):
    db = _Sessao()
    try:
        fatura = db.query(Faturas).filter(Faturas.id == id).first()
        if fatura is None:
            return False

        db.delete(fatura)
        db.commit()

        return True
    finally:
        db.close()

# Transacoes #

def criar_transacao(conta_id, categoria_id, descricao, valor, tipo, categoria, parcelas, data):
    db = _Sessao()

    try:
        transacao = Transacoes(conta_id=conta_id, categoria_id=categoria_id, descricao=descricao, valor=valor, tipo=tipo, Categoria=categoria, parcelas=parcelas, data=data)
        db.add(transacao)
        db.commit()
        db.refresh(transacao)

    finally:
        db.close()

    return transacao

def listar_transacoes():
    db = _Sessao()
    try:
        transacoes = db.query(Transacoes).all()
    finally:
        db.close()
    return transacoes

def buscar_transacao(transacao_id):
    db = _Sessao()
    try:
        transacao = db.query(Transacoes).filter(Transacoes.id == transacao_id).first()
    finally:
        db.close()
    return transacao


def atualizar_transacao(id, conta_id=None, categoria_id=None, descricao=None, valor=None, tipo=None, categoria=None, parcelas=None, data=None):
    db = _Sessao()
    try:
        transacao = db.query(Transacoes).filter(Transacoes.id == id).first()
        if transacao is None:
            return None
        if conta_id is not None:
            transacao.conta_id = conta_id
        if categoria_id is not None:
            transacao.categoria_id = categoria_id
        if descricao is not None:
            transacao.descricao = descricao
        if valor is not None:
            transacao.valor = valor
        if tipo is not None:
            transacao.tipo = tipo
        if categoria is not None:
            transacao.Categoria = categoria
        if parcelas is not None:
            transacao.parcelas = parcelas
        if data is not None:
            transacao.data = data

        db.commit()
        db.refresh(transacao)
        return transacao
    finally:
        db.close()

def excluir_transacao(id):
    db = _Sessao()
    try:
        transacao = db.query(Transacoes).filter(Transacoes.id == id).first()
        if transacao is None:
            return False

        db.delete(transacao)
        db.commit() 
        return True
    finally:
        db.close()


# Investimentos #

def criar_investimento(Nome, Tipo, Valor, transacao_id):
    db = _Sessao()

    try:
        investimento = Investimentos(Nome=Nome, Tipo=Tipo, Valor=Valor, transacao_id=transacao_id)
        db.add(investimento)
        db.commit()
        db.refresh(investimento)

    finally:
        db.close()

    return investimento

def listar_investimentos():
    db = _Sessao()
    try:
        investimentos = db.query(Investimentos).all()
    finally:
        db.close()
    return investimentos

def buscar_investimento(investimento_id):
    db = _Sessao()
    try:
        investimento = db.query(Investimentos).filter(Investimentos.id == investimento_id).first()
    finally:
        db.close()
    return investimento

def atualizar_investimento(id, Nome=None, Tipo=None, Valor=None, transacao_id=None):
    db = _Sessao()
    try:
        investimento = db.query(Investimentos).filter(Investimentos.id == id).first()
        if investimento is None:
            return None
        if Nome is not None:
            investimento.Nome = Nome
        if Tipo is not None:
            investimento.Tipo = Tipo
        if Valor is not None:
            investimento.Valor = Valor
        if transacao_id is not None:
            investimento.transacao_id = transacao_id
        db.commit()
        db.refresh(investimento)
        return investimento
    finally:
        db.close()

def excluir_investimento(id):
    db = _Sessao()
    try:
        investimento = db.query(Investimentos).filter(Investimentos.id == id).first()
        if investimento is None:
            return False

        db.delete(investimento)
        db.commit() 
        return True
    finally:
        db.close()
