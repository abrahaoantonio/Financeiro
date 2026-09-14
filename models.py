from sqlmodel import Field, SQLModel, create_engine
from enum import Enum

class Bancos(Enum):
    NUBANK = "Nubank"
    INTER = "Inter"
    ITAÚ = "Itaú"
    PICPAY = "Picpay"


class Status(Enum):
    ATIVO = "Ativo"
    Inativo = "Inativo"

class Conta(SQLModel, table=True):
    id: int = Field(primary_key=True)
    banco: Bancos = Field(default=Bancos.INTER)
    status: Status = Field(default=Status.ATIVO)
    valor: float


sqlite_file_name = 'database.db'
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


if __name__ == "__main__":  
    SQLModel.metadata.create_all(engine) 