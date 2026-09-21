from sqlmodel import Field, SQLModel, create_engine, Relationship, VARCHAR
from enum import Enum
from datetime import date 

class Bancos(Enum):
    NUBANK = "Nubank"
    INTER = "Inter"
    ITAÚ = "Itaú"
    PICPAY = "Picpay"


class Status(Enum):
    ATIVO = "Ativo"
    Inativo = "Inativo"

class Tipos(Enum):
    ENTRADA = "Entrada"
    SAÍDA = "Saída"



class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    banco: Bancos = Field(default=Bancos.INTER)
    status: Status = Field(default=Status.ATIVO)
    valor: float

class Historico(SQLModel, table=True):
    id: int = Field(primary_key=True)
    conta_id: int = Field(foreign_key="conta.id")
    conta: Conta = Relationship()
    categoria: str
    tipo: Tipos = Field(default=Tipos.ENTRADA)
    valor: float
    data: date= Field(default=date.today())


class Investimento(SQLModel, table=True):
    id: int = Field(primary_key=True)
    nome: str
    categoria: str
    valor: float
    data: date = Field(default=date.today())


sqlite_file_name = 'database.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def criar_tabelas():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":  
    criar_tabelas()
