from flask import Flask
from reactpy import component, html, use_state
from reactpy.backend.flask import configure

from pages.login import PaginaLogin
from pages.usuarios import PaginaUsuarios
from pages.lancar_notas import PaginaLancarNotas
from pages.boletim import PaginaBoletim
from pages.requerimentos import PaginaRequerimentos
from pages.dashboard import dashboard
from components.layout import Layout

app = Flask(__name__)

@component
def AppPrincipal():
    usuario_logado, set_usuario_logado = use_state(None)
    rota, set_rota = use_state("home")

    # Exibe a tela de login sem o layout padrão se não houver usuário logado
    if not usuario_logado:
        return PaginaLogin(on_login_sucesso=set_usuario_logado)

    perfil = usuario_logado.get("perfil")

    # Validação e Roteamento de Conteúdo
    def render_conteudo():
        if rota == "home":
            return dashboard(usuario_logado, set_rota)
        if rota == "usuarios" and perfil == "administrador":
            return PaginaUsuarios()
        if rota == "notas" and perfil in ["professor", "administrador"]:
            return PaginaLancarNotas()
        if rota == "boletim" and perfil == "aluno":
            return PaginaBoletim(usuario_logado)
        if rota == "requerimentos":
            return PaginaRequerimentos(usuario_logado)

        return dashboard(usuario_logado, set_rota)

    def handle_logout():
        set_usuario_logado(None)
        set_rota("home")

    # Aplicação envelopada no Layout Unificado
    return Layout(
        usuario_logado=usuario_logado,
        rota_atual=rota,
        navegar=set_rota,
        on_logout=handle_logout,
        conteudo=render_conteudo()
    )

configure(app, AppPrincipal)

if __name__ == "__main__":
    app.run(debug=True, port=5000)