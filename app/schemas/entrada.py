from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class EntradaCreate(BaseModel):
    codigo_produto: str
    quantidade: int
    observacao: Optional[str] = None

    @field_validator('quantidade')
    @classmethod
    def quantidade_positiva(cls, v):
        if v <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        return v

class EntradaResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    observacao: Optional[str]
    criado_em: datetime
