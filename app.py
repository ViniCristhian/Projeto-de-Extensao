from flask import Flask
from reactpy import component, html, hooks
from reactpy.backend.flask import configure

from database.connection import ler_csv
from pages.usuarios import PaginaUsuarios
from pages.lancar_notas import PaginaLancarNotas
from pages.boletim import PaginaBoletim
from pages.requerimentos import PaginaRequerimentos

app = Flask(__name__)

@component
def AppPrincipal():
    usuario_logado, set_usuario_logado = hooks.use_state(None)
    rota, set_rota = hooks.use_state("home")
    
    login, set_login = hooks.use_state("")
    senha, set_senha = hooks.use_state("")
    erro, set_erro = hooks.use_state("")

    # Tela de Login
    if not usuario_logado:
        def autenticar(e):
            usuarios = ler_csv("usuarios")
            for u in usuarios:
                if u["login"] == login and u["senha"] == senha:
                    set_usuario_logado(u)
                    return
            set_erro("Login ou senha incorretos.")

        return html.div(
            {"style": {"width": "300px", "margin": "100px auto", "font-family": "Arial", "border": "1px solid #ccc", "padding": "20px"}},
            html.h2("Login no Sistema"),
            html.p({"style": {"color": "red"}}, erro),
            html.input({"placeholder": "Login", "value": login, "on_change": lambda e: set_login(e["target"]["value"]), "style": {"width": "100%", "margin-bottom": "10px"}}),
            html.input({"type": "password", "placeholder": "Senha", "value": senha, "on_change": lambda e: set_senha(e["target"]["value"]), "style": {"width": "100%", "margin-bottom": "10px"}}),
            html.button({"on_click": autenticar, "style": {"width": "100%"}}, "Entrar")
        )

    perfil = usuario_logado["perfil"]

    # Roteamento por perfil
    def render_conteudo():
        if rota == "usuarios" and perfil == "administrador": return PaginaUsuarios()
        if rota == "notas" and perfil in ["professor", "administrador"]: return PaginaLancarNotas()
        if rota == "boletim" and perfil == "aluno": return PaginaBoletim(usuario_logado)
        if rota == "requerimentos": return PaginaRequerimentos(usuario_logado)
        return html.div(html.h2(f"Bem-vindo, {usuario_logado['nome']}!"), html.p("Selecione um menu ao lado."))

    # Menu Dinâmico
    botoes = [html.button({"on_click": lambda e: set_rota("home"), "style": {"display": "block", "width": "100%", "margin-bottom": "5px"}}, "Início")]
    if perfil == "administrador":
        botoes.append(html.button({"on_click": lambda e: set_rota("usuarios"), "style": {"display": "block", "width": "100%", "margin-bottom": "5px"}}, "Gestão de Perfis"))
    if perfil in ["professor", "administrador"]:
        botoes.append(html.button({"on_click": lambda e: set_rota("notas"), "style": {"display": "block", "width": "100%", "margin-bottom": "5px"}}, "Lançar Notas"))
    if perfil == "aluno":
        botoes.append(html.button({"on_click": lambda e: set_rota("boletim"), "style": {"display": "block", "width": "100%", "margin-bottom": "5px"}}, "Meu Boletim"))
    
    botoes.append(html.button({"on_click": lambda e: set_rota("requerimentos"), "style": {"display": "block", "width": "100%", "margin-bottom": "5px"}}, "Requerimentos"))
    botoes.append(html.button({"on_click": lambda e: set_usuario_logado(None), "style": {"display": "block", "width": "100%", "margin-top": "20px", "background": "red", "color": "white"}}, "Sair"))

    return html.div(
        {"style": {"display": "flex", "font-family": "Arial", "height": "100vh"}},
        html.div({"style": {"width": "200px", "background": "#f0f0f0", "padding": "15px"}}, botoes),
        html.div({"style": {"flex": "1"}}, render_conteudo())
    )

configure(app, AppPrincipal)

if __name__ == "__main__":
    app.run(debug=True)