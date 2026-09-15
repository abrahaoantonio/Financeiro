from models import Conta, engine, Bancos, Status, Historico, Tipos
from sqlmodel import select, Session
from datetime import date

def criar_conta(conta: Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco==conta.banco)
        resultado = session.exec(statement).all()
        
        if resultado:
            print('Já existe uma conta nesse banco')
            return
        
        session.add(conta)
        session.commit()
        return

def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        resultado = session.exec(statement).all()
    return resultado

def desativar_contas(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id)
        conta =session.exec(statement).first()
        if conta.valor > 0:
            raise ValueError('Essa conta ainda possui saldo')
        conta.status = Status.Inativo
        session.commit()

def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id_conta_saida)
        conta_saida = session.exec(statement).first()
        if conta_saida.valor < valor:
            raise ValueError(f'Saldo insuficiente. Essa conta possui {conta_saida.valor}')
        statement = select(Conta).where(Conta.id==id_conta_entrada)
        conta_entrada = session.exec(statement).first()

        conta_saida.valor -= valor
        conta_entrada.valor += valor

        session.commit()

def movimentar_dinheiro(historico: Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==historico.conta_id)
        conta = session.exec(statement).first()
        if Conta.status == Status.Inativo:
            raise ValueError("A conta está invativa, não tem como prosseguir.")
        else:
            if historico.tipo == Tipos.ENTRADA:
              conta.valor += historico.valor 
            else:
               if conta.valor < historico.valor:
                raise ValueError("Saldo insuficiente")
            conta.valor -= historico.valor

        session.add(historico)
        session.commit()
        return historico

def total_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()

    total = 0
    for conta in contas:
        print(conta.valor)


#transferir_saldo(2,1,4)


historico = Historico(conta_id=2, tipos = Tipos.ENTRADA,categoria="Transferencia pix", valor=4, data=date.today())
movimentar_dinheiro(historico)

