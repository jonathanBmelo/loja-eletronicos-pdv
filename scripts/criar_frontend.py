import os

BASE = r"D:\ESTOQUE - MAIS VENDA\loja-eletronicos\frontend"

index = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Loja de Eletronicos - Login</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f172a; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
    .card { background: #1e293b; padding: 40px; border-radius: 12px; width: 100%; max-width: 400px; box-shadow: 0 20px 60px rgba(0,0,0,0.4); }
    .logo { text-align: center; margin-bottom: 32px; }
    .logo h1 { color: #38bdf8; font-size: 22px; font-weight: 700; }
    .logo p { color: #64748b; font-size: 13px; margin-top: 4px; }
    label { display: block; color: #94a3b8; font-size: 13px; margin-bottom: 6px; margin-top: 16px; }
    input { width: 100%; padding: 10px 14px; background: #0f172a; border: 1px solid #334155; border-radius: 8px; color: #f1f5f9; font-size: 14px; outline: none; }
    input:focus { border-color: #38bdf8; }
    button { width: 100%; margin-top: 24px; padding: 12px; background: #38bdf8; color: #0f172a; border: none; border-radius: 8px; font-size: 15px; font-weight: 700; cursor: pointer; }
    button:hover { background: #0ea5e9; }
    .msg { margin-top: 16px; padding: 10px 14px; border-radius: 8px; font-size: 13px; display: none; }
    .msg.erro { background: #450a0a; color: #fca5a5; display: block; }
    .msg.ok { background: #052e16; color: #86efac; display: block; }
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">
      <h1>Loja de Eletronicos</h1>
      <p>Sistema de Gestao</p>
    </div>
    <label>Email</label>
    <input type="email" id="email" placeholder="admin@loja.com">
    <label>Senha</label>
    <input type="password" id="senha" placeholder="Senha">
    <button onclick="login()">Entrar</button>
    <div class="msg" id="msg"></div>
  </div>
  <script>
    async function login() {
      const email = document.getElementById("email").value;
      const senha = document.getElementById("senha").value;
      const msg = document.getElementById("msg");
      msg.className = "msg";
      msg.textContent = "";
      try {
        const res = await fetch("http://127.0.0.1:8000/auth/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, senha })
        });
        const data = await res.json();
        if (!res.ok) {
          msg.className = "msg erro";
          msg.textContent = data.detail || "Erro ao fazer login";
          return;
        }
        localStorage.setItem("token", data.access_token);
        window.location.href = "cadastro.html";
      } catch (e) {
        msg.className = "msg erro";
        msg.textContent = "Nao foi possivel conectar ao servidor";
      }
    }
    document.addEventListener("keydown", e => { if (e.key === "Enter") login(); });
  </script>
</body>
</html>"""

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(index)

print("index.html criado com sucesso")import os

BASE = r"D:\ESTOQUE - MAIS VENDA\loja-eletronicos\frontend"

cadastro = open(r"D:\ESTOQUE - MAIS VENDA\loja-eletronicos\scripts\cadastro_template.html", encoding="utf-8").read()

with open(os.path.join(BASE, "cadastro.html"), "w", encoding="utf-8") as f:
    f.write(cadastro)

print("cadastro.html criado com sucesso")
