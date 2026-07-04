# Loja de Eletrônicos - Sistema PDV

Sistema de Ponto de Venda (PDV) completo para loja de eletrônicos, desenvolvido com FastAPI, PostgreSQL e Docker.

## Funcionalidades

- **Autenticação** com JWT e controle de acesso por perfil (admin/operador)
- **Cadastro de produtos** com nome, código, preço e endereçamento (corredor/prateleira)
- **Entrada de estoque** com histórico de movimentações
- **Venda** com montagem de NF, múltiplos itens e cálculo de total
- **Formas de pagamento:** PIX, cartão de crédito, cartão de débito e dinheiro (com cálculo de troco)
- **Histórico** de entradas e vendas com detalhamento de itens
- **Busca** de produtos por nome ou código

## Tecnologias

- **Backend:** Python 3.14, FastAPI, Psycopg3
- **Banco de dados:** PostgreSQL 15
- **Autenticação:** JWT (python-jose), Bcrypt
- **Infraestrutura:** Docker, Docker Compose
- **Frontend:** HTML, CSS e JavaScript puro

## Estrutura do projeto
loja-eletronicos/
├── app/
│   ├── auth/          # JWT e hash de senha
│   ├── models/        # Criação das tabelas
│   ├── routes/        # Endpoints da API
│   └── schemas/       # Validação com Pydantic
├── frontend/          # Telas HTML do sistema
├── scripts/           # Scripts utilitários
├── docker-compose.yml
└── requirements.txt

## Como rodar

**Pré-requisitos:** Python 3.10+, Docker Desktop

1. Clone o repositório
```bash
git clone https://github.com/jonathanBmelo/loja-eletronicos-pdv.git
cd loja-eletronicos-pdv
```

2. Crie o arquivo `.env` na raiz com as variáveis:
```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=loja
DB_USER=admin
DB_PASSWORD=admin123
SECRET_KEY=sua_chave_secreta_aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

3. Suba o banco de dados
```bash
docker compose up -d
```

4. Crie o ambiente virtual e instale as dependências
```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

5. Suba a API
```bash
uvicorn app.main:app --reload
```

6. Acesse o sistema em `http://127.0.0.1:8000/static/index.html`

## Rotas da API

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | /auth/registrar | Cadastrar usuário |
| POST | /auth/login | Login e geração de token |
| GET | /produtos/ | Listar produtos |
| POST | /produtos/ | Cadastrar produto |
| PATCH | /produtos/{codigo} | Editar produto |
| GET | /produtos/buscar/?q= | Buscar por nome ou código |
| POST | /entradas/ | Registrar entrada de estoque |
| GET | /entradas/ | Listar entradas |
| POST | /vendas/ | Finalizar venda |
| GET | /vendas/ | Listar vendas |
| GET | /vendas/{id} | Detalhes de uma venda |

## Autor

Jonathan Bezerra de Melo — [GitHub](https://github.com/jonathanBmelo)