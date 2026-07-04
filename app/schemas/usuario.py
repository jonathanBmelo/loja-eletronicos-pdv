from pydantic import BaseModel, field_validator
from typing import Optional

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    role: Optional[str] = "operador"

    @field_validator("role")
    @classmethod
    def role_valida(cls, v):
        if v not in ("admin", "operador"):
            raise ValueError("Role deve ser admin ou operador")
        return v

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    role: str
    ativo: bool

class LoginRequest(BaseModel):
    email: str
    senha: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str