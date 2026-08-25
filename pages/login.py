from reactpy import component, html, use_state
from database.connection import autenticar_usuario

@component
def PaginaLogin(on_login_sucesso):
    login, set_login = use_state("")
    senha, set_senha = use_state("")
    erro, set_erro = use_state("")

    def handle_autenticar(e):
        usuario = autenticar_usuario(login.strip(), senha.strip())
        if usuario:
            set_erro("")
            on_login_sucesso(usuario)
        else:
            set_erro("Login ou senha incorretos.")

    return html.div(
        {"style": {
            "width": "320px",
            "margin": "100px auto",
            "fontFamily": "sans-serif",
            "border": "1px solid #e2e8f0",
            "padding": "24px",
            "borderRadius": "8px",
            "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
        }},
        html.h2({"style": {"textAlign": "center", "marginBottom": "20px"}}, "Login no Sistema"),
        html.p({"style": {"color": "#ef4444", "fontSize": "0.875rem", "minHeight": "20px"}}, erro),
        html.div(
            {"style": {"display": "flex", "flexDirection": "column", "gap": "12px"}},
            html.input({
                "placeholder": "Login",
                "value": login,
                "on_change": lambda e: set_login(e["target"]["value"]),
                "style": {"padding": "8px", "borderRadius": "4px", "border": "1px solid #ccc"}
            }),
            html.input({
                "type": "password",
                "placeholder": "Senha",
                "value": senha,
                "on_change": lambda e: set_senha(e["target"]["value"]),
                "style": {"padding": "8px", "borderRadius": "4px", "border": "1px solid #ccc"}
            }),
            html.button({
                "on_click": handle_autenticar,
                "style": {"padding": "10px", "background": "#2563eb", "color": "white", "border": "none", "borderRadius": "4px", "cursor": "pointer"}
            }, "Entrar")
        )
    )