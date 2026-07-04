from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.schemas.entrada import EntradaCreate, EntradaResponse
from app.auth.jwt import verificar_token
from app.database import get_connection

router = APIRouter(prefix='/entradas', tags=['entradas'])

def exigir_admin(authorization: str):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Token nao fornecido')
    payload = verificar_token(authorization.split(' ')[1])
    if not payload:
        raise HTTPException(status_code=401, detail='Token invalido ou expirado')
    if payload.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Acesso restrito a administradores')
    return payload

@router.post('/', response_model=EntradaResponse)
def registrar_entrada(entrada: EntradaCreate, authorization: Optional[str] = Header(None)):
    exigir_admin(authorization)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id FROM produtos WHERE codigo = %s', (entrada.codigo_produto,))
            produto = cur.fetchone()
            if not produto:
                raise HTTPException(status_code=404, detail='Produto nao encontrado')
            cur.execute('''
                INSERT INTO entradas (produto_id, quantidade, observacao)
                VALUES (%s, %s, %s)
                RETURNING id, produto_id, quantidade, observacao, criado_em
            ''', (produto['id'], entrada.quantidade, entrada.observacao))
            nova_entrada = cur.fetchone()
            cur.execute('''
                UPDATE produtos SET quantidade = quantidade + %s WHERE id = %s
            ''', (entrada.quantidade, produto['id']))
        conn.commit()
    return nova_entrada

@router.get('/', response_model=list[EntradaResponse])
def listar_entradas(authorization: Optional[str] = Header(None)):
    exigir_admin(authorization)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, produto_id, quantidade, observacao, criado_em FROM entradas ORDER BY criado_em DESC')
            return cur.fetchall()
