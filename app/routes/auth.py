from fastapi import APIRouter, HTTPException
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, LoginRequest, TokenResponse
from app.auth.hashing import hash_senha, verificar_senha
from app.auth.jwt import criar_token
from app.database import get_connection

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/registrar", response_model=UsuarioResponse)
def registrar(usuario: UsuarioCreate):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM usuarios WHERE email = %s", (usuario.email,))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Email ja cadastrado")
            cur.execute("""
                INSERT INTO usuarios (nome, email, senha_hash, role)
                VALUES (%s, %s, %s, %s)
                RETURNING id, nome, email, role, ativo
            """, (usuario.nome, usuario.email, hash_senha(usuario.senha), usuario.role))
            novo = cur.fetchone()
        conn.commit()
    return novo

@router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM usuarios WHERE email = %s AND ativo = TRUE", (dados.email,))
            usuario = cur.fetchone()
    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais invalidas")
    if not verificar_senha(dados.senha, usuario["senha_hash"]):
        raise HTTPException(status_code=401, detail="Credenciais invalidas")
    token = criar_token({"sub": usuario["email"], "role": usuario["role"]})
    return {"access_token": token, "token_type": "bearer"}