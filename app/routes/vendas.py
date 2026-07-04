from fastapi import APIRouter, HTTPException, Header
from typing import Optional
from app.schemas.venda import VendaCreate, VendaResponse
from app.auth.jwt import verificar_token
from app.database import get_connection

router = APIRouter(prefix='/vendas', tags=['vendas'])

def obter_usuario(authorization: str):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail='Token nao fornecido')
    payload = verificar_token(authorization.split(' ')[1])
    if not payload:
        raise HTTPException(status_code=401, detail='Token invalido ou expirado')
    return payload

@router.post('/', response_model=VendaResponse)
def finalizar_venda(venda: VendaCreate, authorization: Optional[str] = Header(None)):
    obter_usuario(authorization)
    formas_validas = ['dinheiro', 'pix', 'cartao_credito', 'cartao_debito']
    if venda.forma_pagamento not in formas_validas:
        raise HTTPException(status_code=400, detail='Forma de pagamento invalida')
    with get_connection() as conn:
        with conn.cursor() as cur:
            itens_processados = []
            total = 0
            for item in venda.itens:
                cur.execute('SELECT id, preco, quantidade FROM produtos WHERE codigo = %s', (item.codigo_produto,))
                produto = cur.fetchone()
                if not produto:
                    raise HTTPException(status_code=404, detail=f'Produto {item.codigo_produto} nao encontrado')
                subtotal = float(produto['preco']) * item.quantidade
                total += subtotal
                itens_processados.append({
                    'produto_id': produto['id'],
                    'quantidade': item.quantidade,
                    'preco_unit': float(produto['preco']),
                    'subtotal': subtotal
                })
            cur.execute('''
                INSERT INTO vendas (total, forma_pagamento)
                VALUES (%s, %s) RETURNING id, total, forma_pagamento, criado_em
            ''', (total, venda.forma_pagamento))
            nova_venda = cur.fetchone()
            venda_id = nova_venda['id']
            itens_resp = []
            for it in itens_processados:
                cur.execute('''
                    INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unit, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, produto_id, quantidade, preco_unit, subtotal
                ''', (venda_id, it['produto_id'], it['quantidade'], it['preco_unit'], it['subtotal']))
                itens_resp.append(cur.fetchone())
                cur.execute('UPDATE produtos SET quantidade = quantidade - %s WHERE id = %s',
                    (it['quantidade'], it['produto_id']))
        conn.commit()
    return {**nova_venda, 'itens': itens_resp}

@router.get('/', response_model=list[VendaResponse])
def listar_vendas(authorization: Optional[str] = Header(None)):
    obter_usuario(authorization)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, total, forma_pagamento, criado_em FROM vendas ORDER BY criado_em DESC')
            return cur.fetchall()

@router.get('/{venda_id}', response_model=VendaResponse)
def buscar_venda(venda_id: int, authorization: Optional[str] = Header(None)):
    obter_usuario(authorization)
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, total, forma_pagamento, criado_em FROM vendas WHERE id = %s', (venda_id,))
            venda = cur.fetchone()
            if not venda:
                raise HTTPException(status_code=404, detail='Venda nao encontrada')
            cur.execute('SELECT iv.id, iv.produto_id, p.nome as nome_produto, iv.quantidade, iv.preco_unit, iv.subtotal FROM itens_venda iv JOIN produtos p ON p.id = iv.produto_id WHERE iv.venda_id = %s', (venda_id,))
            itens = cur.fetchall()
    return {**venda, 'itens': itens}
