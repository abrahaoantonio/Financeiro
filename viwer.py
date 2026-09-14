from models import Conta, engine, Bancos
from sqlmodel import select, Session

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

conta = Conta(valor=5, banco=Bancos.NUBANK)
criar_conta(conta)
