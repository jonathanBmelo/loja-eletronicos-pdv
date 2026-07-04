from app.database import get_connection

def criar_tabela_usuarios():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id          SERIAL PRIMARY KEY,
                    nome        VARCHAR(100) NOT NULL,
                    email       VARCHAR(100) NOT NULL UNIQUE,
                    senha_hash  TEXT NOT NULL,
                    role        VARCHAR(20) NOT NULL DEFAULT 'operador',
                    ativo       BOOLEAN NOT NULL DEFAULT TRUE,
                    criado_em   TIMESTAMP DEFAULT NOW()
                )
            """)
        conn.commit()