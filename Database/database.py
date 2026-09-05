from sqlalchemy import ForeignKey, create_engine, Column, String, Integer, Numeric, Date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


engine = create_engine('sqlite:///Financeiro.db')
Base = declarative_base()
_Sessao = sessionmaker(bind=engine,autoflush=False,autocommit=False)



######     CONTA     ######


class Conta(Base):

    __tablename__ = 'contas'


    id = Column(Integer, primary_key=True)
    nome = Column(String(40), unique=True, nullable=False)
    tipo = Column(String(40))
    saldo = Column(Numeric(10, 2), default=0.00)
    data_criação = Column(Date)

    cartoes = relationship(
        "Cartoes",
        back_populates="conta")   # <-- Relacionamento com a tabela Cartões

    transacoes = relationship(
        "Transacoes",
        back_populates="conta") # <-- Relacionamento com a tabela Transações

    parcelamentos = relationship('parcelamentos', back_populates='contas')

    def __repr__(self):
        return f"Conta(id={self.id}, nome='{self.nome}', tipo='{self.tipo}', saldo={self.saldo}, data_criação='{self.data_criação}')"


######     CATEGORIAS     ######


class Categorias(Base):

    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nome = Column(String(40), unique=True, nullable=False)
    tipo = Column(String(40))

    transacoes = relationship(
        "Transacoes",
        back_populates="categoria"
    )

    def __repr__(self):
        return f"Categorias(id={self.id}, nome='{self.nome}', tipo='{self.tipo}')"



#####     TRANSAÇÕES     ######


class Transacoes(Base):

    __tablename__ = 'transacoes'

    id = Column(Integer, primary_key=True)
    conta_id = Column(Integer, ForeignKey("contas.id"))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    fatura_id = Column(Integer, ForeignKey("Faturas.id"))
    descricao = Column(String(100))
    valor = Column(Numeric(10, 2), default=00.0)
    tipo = Column(String(40))
    Categoria = Column(String(40))
    parcelas = Column(Integer)
    data = Column(String(40))

    conta = relationship(
        "Conta",
        back_populates="transacoes"
    )   # <-- Relacionamento com a tabela Contas

    categoria = relationship(
        "Categorias",
        back_populates="transacoes"
    )   # <-- Relacionamento com a tabela Categorias

    investimentos = relationship(
        "Investimentos",
        back_populates="transacoes"
    )

    fatura = relationship("Faturas", back_populates="transacoes")

    def __repr__(self):
        return f"Transacoes(id={self.id}, conta_id={self.conta_id}, categoria_id={self.categoria_id}, descricao='{self.descricao}', valor={self.valor}, tipo='{self.tipo}', Categoria='{self.Categoria}', parcelas={self.parcelas}, data='{self.data}')"



#####     CARTÕES    ##### 


class Cartoes(Base):

    __tablename__ = 'cartoes'

    id = Column(Integer, primary_key=True)
    conta_id = Column(Integer,ForeignKey("contas.id"))
    categoria_id = Column(Integer,ForeignKey("categorias.id"))
    limite = Column(Numeric(10,2))
    descricao = Column(String(100))
    valor = Column(Numeric(10, 2), default= 00.0)
    tipo = Column(String(40))
    dia_fechamento = Column(Date)
    dia_vencimento = Column(Date)

    conta = relationship(
        "Conta",
        back_populates="cartoes"
    )  #<-- Relacionamento com a tabela Contas

    categoria = relationship(
        "Categoria",
        back_populates="cartoes"
    )  # <-- Relacionamento com a tabela Faturas

    faturas = relationship("Faturas",back_populates="cartoes")

    parcelamentos = relationship('parcelamentos', back_populates='cartoes')

    def __repr__(self):
        return f"Cartoes(id={self.id}, Nome='{self.Nome}', Limite={self.Limite}, dia_fechamento='{self.dia_fechamento}', dia_vencimento='{self.dia_vencimento}', contas_id={self.contas_id})"




# FATURAS #


class Faturas(Base):

    __tablename__ = 'Faturas'

    id = Column(Integer, primary_key=True)
    cartao_id = Column(Integer, ForeignKey("cartoes.id"))
    Mês = Column(String(40))
    Ano = Column(String(40))
    Valor = Column(Numeric(10, 2), default=00.0)
    data_vencimento = Column(String(40))
    data_fechamento = Column(String(40))
    Status = Column(String(40))

    cartao = relationship(
        "Cartoes",
        back_populates="faturas"
    )  # <-- Relacionamento com a tabela Cartões

    transacoes = relationship("Transacoes", back_populates="fatura")

    def __repr__(self):
        return f"Faturas(id={self.id}, cartao_id={self.cartao_id}, Mês='{self.Mês}', Ano='{self.Ano}', Valor={self.Valor}, data_vencimento='{self.data_vencimento}', Status='{self.Status}')"




# Investimentos #

class Investimentos(Base):

    __tablename__ = 'Investimentos'

    id = Column(Integer, primary_key=True)
    nome = Column(String(40), unique=True, nullable=False)
    tipo = Column(String(40))   
    Valor = Column(Numeric(10, 2))
    transacao_id = Column(Integer, ForeignKey("transacoes.id"))

    transacao = relationship("Transacoes", back_populates="investimentos")  # <-- Relacionamento com a tabela Transações


class Parcelamento(Base):
    __tablename__ = "parcelamentos"

    id = Column(Integer, primary_key=True)
    descricao = Column(String, nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False)
    quantidade_parcelas = Column(Integer, nullable=False)
    data_inicio = Column(Date, nullable=False)
    cartao_id = Column(Integer, ForeignKey("cartoes.id"), nullable=True)
    conta_id = Column(Integer, ForeignKey("contas.id"), nullable=True)

    parcelas = relationship("parcelas", back_populates="parcelamentos")

    cartao = relationship('cartoes', back_populates='parcelamentos')

    conta = relationship('conta', back_populates='parcelamentos')

    def __repr__(self):
            return f"parcelamentos(id={self.id}, descricao={self.descricao}, valor_total='{self.valor_total}', quantidade_parcelas='{self.quantidade_parcelas}', data_inicio={self.data_inicio}, cartao_id='{self.cartao_id}', conta_id ='{self.conta_id }')"


class Parcela(Base):
    __tablename__ = "parcelas"

    id = Column(Integer, primary_key=True)
    parcelamento_id = Column(Integer,ForeignKey("parcelamentos.id"),nullable=False)
    numero = Column(Integer, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    vencimento = Column(Date, nullable=False)
    status = Column(String, default="Pendente")

    parcelamentos = relationship('parcelamentos', back_populates='parcelas')


Base.metadata.create_all(engine)



