from models import Conta, engine, Bancos, Status, Historico, Investimento, Tipos
from sqlmodel import select, Session
from datetime import date, timedelta
import matplotlib.pyplot as plt

def criar_conta(conta: Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco==conta.banco)
        resultado = session.exec(statement).all()
        
        if resultado:
            raise ValueError('Já existe uma conta nesse banco')
        
        session.add(conta)
        session.commit()
        return

def listar_contas():
    with Session(engine) as session:
        statement = select(Conta)
        resultado = session.exec(statement).all()
    return resultado


def proximo_id_conta():
    contas = listar_contas()
    return max((conta.id for conta in contas), default=0) + 1


def proximo_id_historico():
    with Session(engine) as session:
        ids = session.exec(select(Historico.id)).all()
    return max(ids, default=0) + 1


def proximo_id_investimento():
    with Session(engine) as session:
        ids = session.exec(select(Investimento.id)).all()
    return max(ids, default=0) + 1


def excluir_conta(id_conta):
    with Session(engine) as session:
        conta = session.get(Conta, id_conta)
        if not conta:
            raise ValueError("Conta não encontrada")
        if conta.valor != 0:
            raise ValueError("A conta precisa estar com saldo zero para ser excluída")
        possui_historico = session.exec(
            select(Historico).where(Historico.conta_id == id_conta)
        ).first()
        if possui_historico:
            raise ValueError("Esta conta possui movimentações e não pode ser excluída")
        session.delete(conta)
        session.commit()

def desativar_contas(id):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id)
        conta =session.exec(statement).first()
        if conta.valor > 0:
            raise ValueError('Essa conta ainda possui saldo')
        conta.status = Status.Inativo
        session.commit()

def transferir_saldo(id_conta_saida, id_conta_entrada, valor):
    if valor <= 0:
        raise ValueError('O valor da transferência deve ser maior que zero')
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id_conta_saida)
        conta_saida = session.exec(statement).first()
        if not conta_saida:
            raise ValueError('Conta de origem não encontrada')
        if conta_saida.status != Status.ATIVO:
            raise ValueError('A conta de origem está inativa')
        if conta_saida.valor < valor:
            raise ValueError(f'Saldo insuficiente. Essa conta possui {conta_saida.valor}')
        statement = select(Conta).where(Conta.id==id_conta_entrada)
        conta_entrada = session.exec(statement).first()
        if not conta_entrada:
            raise ValueError('Conta de destino não encontrada')
        if conta_entrada.status != Status.ATIVO:
            raise ValueError('A conta de destino está inativa')

        conta_saida.valor -= valor
        conta_entrada.valor += valor

        session.commit()

def movimentar_dinheiro(historico: Historico):
    if historico.valor <= 0:
        raise ValueError('O valor da movimentação deve ser maior que zero')
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==historico.conta_id)
        conta = session.exec(statement).first()
        if not conta:
            raise ValueError('Conta não encontrada')
        if conta.status != Status.ATIVO:
            raise ValueError('A conta está inativa')
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
        total += conta.valor

    return float(total)


def buscar_historico_entre_datas(data_inicio: date, data_fim: date):
    with Session(engine) as session:
        statement = select(Historico).where(Historico.data >= data_inicio, 
                                            Historico.data <= data_fim)
        resultados = session.exec(statement).all()
        return resultados


def resumo_entradas_saidas():
    totais = {"Entrada": 0.0, "Saída": 0.0}
    with Session(engine) as session:
        historicos = session.exec(select(Historico)).all()
    for historico in historicos:
        chave = "Entrada" if historico.tipo == Tipos.ENTRADA else "Saída"
        totais[chave] += historico.valor
    return totais


def gastos_por_categoria():
    gastos = {}
    with Session(engine) as session:
        saidas = session.exec(
            select(Historico).where(Historico.tipo != Tipos.ENTRADA)
        ).all()
    for saida in saidas:
        gastos[saida.categoria] = gastos.get(saida.categoria, 0.0) + saida.valor
    return gastos


def registrar_investimento(investimento: Investimento):
    if investimento.valor <= 0:
        raise ValueError("O valor do investimento deve ser maior que zero")
    with Session(engine) as session:
        session.add(investimento)
        session.commit()
    return investimento


def excluir_investimento(id_investimento):
    with Session(engine) as session:
        investimento = session.get(Investimento, id_investimento)
        if not investimento:
            raise ValueError("Investimento não encontrado")
        session.delete(investimento)
        session.commit()


def listar_investimentos():
    with Session(engine) as session:
        return session.exec(select(Investimento).order_by(Investimento.data)).all()


def total_investimentos():
    return sum(investimento.valor for investimento in listar_investimentos())


def evolucao_investimentos():
    total_acumulado = 0.0
    evolucao = []
    for investimento in listar_investimentos():
        total_acumulado += investimento.valor
        evolucao.append((investimento.data, total_acumulado))
    return evolucao


def investimentos_por_categoria():
    totais = {}
    for investimento in listar_investimentos():
        totais[investimento.categoria] = totais.get(investimento.categoria, 0.0) + investimento.valor
    return totais

#x = buscar_historico_entre_datas(date.today() - timedelta(days=1), date.today() + timedelta(days=1))

def criar_grafico_movimentacao():
    with Session(engine) as session:
        statement = select(Historico)
        historico = session.exec(statement).all()
        tipos = [i.tipo.value for i in historico]
        valores = [i.valor for i in historico]


        plt.bar(tipos, valores)
        plt.show()

def criar_grafico_conta():
    with Session(engine) as session:
        statement = select(Conta).where(Conta.status==Status.ATIVO)
        contas = session.exec(statement).all()
        bancos = [i.banco.value for i in contas]
        total = [i.valor for i in contas]

        plt.bar(bancos, total)
        plt.show()




#criar_grafico_conta()

