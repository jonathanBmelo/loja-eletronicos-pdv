from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ItemVendaInput(BaseModel):
    codigo_produto: str
    quantidade: int

class VendaCreate(BaseModel):
    itens: list[ItemVendaInput]
    forma_pagamento: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

class ItemVendaResponse(BaseModel):
    id: int
    produto_id: int
    nome_produto: Optional[str] = None
    quantidade: int
    preco_unit: float
    subtotal: float

class VendaResponse(BaseModel):
    id: int
    total: float
    forma_pagamento: str
    criado_em: datetime
    itens: Optional[list[ItemVendaResponse]] = None
