from app.database import get_connection

def criar_tabelas_venda():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS vendas (
                    id              SERIAL PRIMARY KEY,
                    total           NUMERIC(10,2) NOT NULL,
                    forma_pagamento VARCHAR(20) NOT NULL,
                    criado_em       TIMESTAMP DEFAULT NOW()
                )
            ''')
            cur.execute('''
                CREATE TABLE IF NOT EXISTS itens_venda (
                    id          SERIAL PRIMARY KEY,
                    venda_id    INTEGER NOT NULL REFERENCES vendas(id),
                    produto_id  INTEGER NOT NULL REFERENCES produtos(id),
                    quantidade  INTEGER NOT NULL,
                    preco_unit  NUMERIC(10,2) NOT NULL,
                    subtotal    NUMERIC(10,2) NOT NULL
                )
            ''')
        conn.commit()
