from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, produtos, entradas, vendas
from app.models.produto import criar_tabela_produtos
from app.models.usuario import criar_tabela_usuarios
from app.models.entrada import criar_tabela_entradas
from app.models.venda import criar_tabelas_venda

app = FastAPI(
    title='Loja de Eletronicos',
    description='Sistema de vendas integrado ao estoque',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
def startup():
    criar_tabela_usuarios()
    criar_tabela_produtos()
    criar_tabela_entradas()
    criar_tabelas_venda()

from fastapi.staticfiles import StaticFiles
app.mount('/static', StaticFiles(directory='frontend'), name='static')

app.include_router(auth.router)
app.include_router(produtos.router)
app.include_router(entradas.router)
app.include_router(vendas.router)

@app.get('/')
def root():
    return {'status': 'online', 'sistema': 'Loja de Eletronicos'}
