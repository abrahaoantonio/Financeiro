from sqlalchemy import create_engine, Column, String, Integer, Numeric, Date
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///Financeiro.db')
Base = declarative_base()
_Sessao = sessionmaker(engine)


class Conta(Base):

    __tablename__ = 'Contas'


    id = Column(Integer, primary_key=True)
    nome = Column(String(40), unique=True, nullable=False)
    tipo = Column(String(40))
    saldo = Column(Numeric(10, 2))
    data_criação = Column(String(40))

    def __repr__(self):
        return f"Conta(id={self.id}, nome='{self.nome}', tipo='{self.tipo}', saldo={self.saldo}, data_criação='{self.data_criação}')"

Base.metadata.create_all(engine)   

with _Sessao() as sessao:
    conta1 = Conta(nome='Inter', tipo='Corrente', saldo=1474.90, data_criação='2026-09-01')
    sessao.add(conta1)
    sessao.commit()


class Categorias(Base):

    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nome = Column(String(40), unique=True, nullable=False)
    tipo = Column(String(40))

    def __repr__(self):
        return f"Categorias(id={self.id}, nome='{self.nome}', tipo='{self.tipo}')"

Base.metadata.create_all(engine)

with _Sessao() as sessao:
    categoria1 = Categorias(nome='Alimentação', tipo='Despesa')
    sessao.add(categoria1)
    categoria2 = Categorias(nome='Salário', tipo='Receita')
    sessao.add(categoria2)
    categoria3 = Categorias(nome='Transporte', tipo='Despesa')
    sessao.add(categoria3)
    categoria4 = Categorias(nome='Investimentos', tipo='investimento')
    sessao.add(categoria4)
    categoria5 = Categorias(nome='Lazer', tipo='Despesa')
    sessao.add(categoria5)  
    sessao.commit()


class Transacoes(Base):

    __tablename__ = 'Transações'

    id = Column(Integer, primary_key=True)
    conta_id = Column(Integer)
    categoria_id = Column(Integer)
    descricao = Column(String(100))
    valor = Column(Numeric(10, 2))
    tipo = Column(String(40))
    tipo_transacao = Column(String(40))
    parcelas = Column(Integer)
    data = Column(String(40))

    def __repr__(self):
        return f"Transacoes(id={self.id}, conta_id={self.conta_id}, categoria_id={self.categoria_id}, descricao='{self.descricao}', valor={self.valor}, tipo='{self.tipo}', tipo_transacao='{self.tipo_transacao}', parcelas={self.parcelas}, data='{self.data}')"


Base.metadata.create_all(engine)

with _Sessao() as sessao:
    transacao1 = Transacoes(conta_id=1, categoria_id=1, descricao='Compra no supermercado', valor=150.00, tipo='Despesa', tipo_transacao='Débito', parcelas=1, data='2026-09-03')
    sessao.add(transacao1)
    sessao.commit()




