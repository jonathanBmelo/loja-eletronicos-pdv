from app.database import get_connection

def criar_tabela_produtos():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id          SERIAL PRIMARY KEY,
                    nome        VARCHAR(100) NOT NULL,
                    codigo      VARCHAR(50)  NOT NULL UNIQUE,
                    preco       NUMERIC(10,2) NOT NULL,
                    corredor    VARCHAR(20),
                    prateleira  VARCHAR(20),
                    quantidade  INTEGER NOT NULL DEFAULT 0,
                    criado_em   TIMESTAMP DEFAULT NOW()
                )
            """)
        conn.commit()