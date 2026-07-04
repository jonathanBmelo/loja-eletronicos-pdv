from app.database import get_connection

def criar_tabela_entradas():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS entradas (
                    id           SERIAL PRIMARY KEY,
                    produto_id   INTEGER NOT NULL REFERENCES produtos(id),
                    quantidade   INTEGER NOT NULL CHECK (quantidade > 0),
                    observacao   TEXT,
                    criado_em    TIMESTAMP DEFAULT NOW()
                )
            ''')
        conn.commit()
