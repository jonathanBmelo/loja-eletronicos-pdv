Set-Location "D:\ESTOQUE - MAIS VENDA\loja-eletronicos"
& "D:\ESTOQUE - MAIS VENDA\loja-eletronicos\venv\Scripts\Activate.ps1"
uvicorn app.main:app --reload