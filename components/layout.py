from reactpy import component, html
from components.header import Header
from components.footer import Footer

@component
def Layout(usuario_logado, rota_atual, navegar, on_logout, conteudo):
    return html.div(
        {"style": {
            "display": "flex",
            "flexDirection": "column",
            "minHeight": "100vh",
            "fontFamily": "system-ui, -apple-system, sans-serif",
            "background": "#f8fafc"
        }},
        Header(
            usuario_logado=usuario_logado,
            rota_atual=rota_atual,
            navegar=navegar,
            on_logout=on_logout
        ),
        html.main(
            {"style": {
                "flex": "1",
                "padding": "2rem",
                "maxWidth": "1200px",
                "width": "100%",
                "margin": "0 auto"
            }},
            conteudo
        ),
        Footer()
    )