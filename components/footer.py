from reactpy import component, html

@component
def Footer():
    return html.footer(
        {"style": {
            "background": "#0f172a",
            "color": "#94a3b8",
            "textAlign": "center",
            "padding": "1rem",
            "marginTop": "auto",
            "fontSize": "0.85rem",
            "borderTop": "1px solid #1e293b"
        }},
        html.p({"style": {"margin": "0"}}, "Sistema Escolar © Todos os direitos reservados.")
    )