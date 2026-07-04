from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from app.auth.jwt import verificar_token
from app.database import get_connection

router = APIRouter(prefix="/produtos", tags=["produtos"])

def obter_usuario_token(authorization: str):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token nao fornecido")
    token = authorization.split(" ")[1]
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token invalido ou expirado")
    return payload

def exigir_admin(authorization: str):
    payload = obter_usuario_token(authorization)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return payload

@router.post("/", response_model=ProdutoResponse)
def cadastrar_produto(produto: ProdutoCreate, authorization: Optional[str] = Header(None)):
    exigir_admin(authorization)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM produtos WHERE codigo = %s", (produto.codigo,))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="Codigo ja cadastrado")
            cur.execute("""
                INSERT INTO produtos (nome, codigo, preco, corredor, prateleira)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, nome, codigo, preco, corredor, prateleira, quantidade
            """, (produto.nome, produto.codigo, produto.preco, produto.corredor, produto.prateleira))
            novo = cur.fetchone()
        conn.commit()
    return novo

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(authorization: Optional[str] = Header(None)):
    obter_usuario_token(authorization)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome, codigo, preco, corredor, prateleira, quantidade FROM produtos ORDER BY nome")
            return cur.fetchall()

@router.get("/{codigo}", response_model=ProdutoResponse)
def buscar_produto(codigo: str, authorization: Optional[str] = Header(None)):
    obter_usuario_token(authorization)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, nome, codigo, preco, corredor, prateleira, quantidade FROM produtos WHERE codigo = %s", (codigo,))
            produto = cur.fetchone()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    return produto

@router.patch("/{codigo}", response_model=ProdutoResponse)
def editar_produto(codigo: str, dados: ProdutoUpdate, authorization: Optional[str] = Header(None)):
    exigir_admin(authorization)
    campos = {k: v for k, v in dados.model_dump().items() if v is not None}
    if not campos:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")
    set_clause = ", ".join(f"{k} = %s" for k in campos)
    valores = list(campos.values()) + [codigo]
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(f"UPDATE produtos SET {set_clause} WHERE codigo = %s RETURNING id, nome, codigo, preco, corredor, prateleira, quantidade", valores)
            atualizado = cur.fetchone()
        conn.commit()
    if not atualizado:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    return atualizado
@router.get("/buscar/", response_model=list[ProdutoResponse])
def buscar_produtos(q: str, authorization: Optional[str] = Header(None)):
    obter_usuario_token(authorization)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, nome, codigo, preco, corredor, prateleira, quantidade 
                FROM produtos 
                WHERE nome ILIKE %s OR codigo ILIKE %s
                ORDER BY nome
            """, (f"%{q}%", f"%{q}%"))
            return cur.fetchall()