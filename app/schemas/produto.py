from pydantic import BaseModel, field_validator
from typing import Optional

class ProdutoCreate(BaseModel):
    nome: str
    codigo: str
    preco: float
    corredor: Optional[str] = None
    prateleira: Optional[str] = None

    @field_validator("preco")
    @classmethod
    def preco_positivo(cls, v):
        if v <= 0:
            raise ValueError("Preco deve ser maior que zero")
        return v

    @field_validator("nome", "codigo")
    @classmethod
    def nao_vazio(cls, v):
        if not v.strip():
            raise ValueError("Campo nao pode ser vazio")
        return v.strip()

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    preco: Optional[float] = None
    corredor: Optional[str] = None
    prateleira: Optional[str] = None

    @field_validator("preco")
    @classmethod
    def preco_positivo(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Preco deve ser maior que zero")
        return v

class ProdutoResponse(BaseModel):
    id: int
    nome: str
    codigo: str
    preco: float
    corredor: Optional[str]
    prateleira: Optional[str]
    quantidade: int