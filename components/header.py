from reactpy import component, html

@component
def Header(usuario_logado, rota_atual, navegar, on_logout):
    perfil = usuario_logado.get("perfil")

    # Mapeamento de links por permissão de acesso
    links = [("home", "Início")]

    if perfil == "administrador":
        links.append(("usuarios", "Gestão de Perfis"))
    if perfil in ["professor", "administrador"]:
        links.append(("notas", "Lançar Notas"))
    if perfil == "aluno":
        links.append(("boletim", "Meu Boletim"))

    links.append(("requerimentos", "Requerimentos"))

    return html.header(
        {"style": {
            "background": "#1e293b",
            "color": "#ffffff",
            "padding": "0.8rem 2rem",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "space-between",
            "flexWrap": "wrap",
            "gap": "1rem",
            "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
        }},
        # Título
        html.h1({"style": {"margin": "0", "fontSize": "1.25rem", "fontWeight": "600"}}, "Sistema Escolar"),

        # Menu de Navegação Superior
        html.nav(
            {"style": {"display": "flex", "gap": "0.4rem", "alignItems": "center", "flexWrap": "wrap"}},
            [
                html.button(
                    {
                        "key": chave,
                        "on_click": lambda e, c=chave: navegar(c),
                        "style": {
                            "background": "#2563eb" if rota_atual == chave else "transparent",
                            "color": "#ffffff",
                            "border": "none",
                            "padding": "0.4rem 0.8rem",
                            "borderRadius": "6px",
                            "cursor": "pointer",
                            "fontSize": "0.875rem",
                            "fontWeight": "500"
                        }
                    },
                    rotulo
                ) for chave, rotulo in links
            ]
        ),

        # Informações da Conta e Ação de Sair
        html.div(
            {"style": {"display": "flex", "alignItems": "center", "gap": "1rem"}},
            html.span(
                {"style": {"fontSize": "0.85rem", "color": "#cbd5e1"}},
                f"👤 {usuario_logado.get('nome', 'Usuário')} ({perfil})"
            ),
            html.button(
                {
                    "on_click": lambda e: on_logout(),
                    "style": {
                        "background": "#ef4444",
                        "color": "#ffffff",
                        "border": "none",
                        "padding": "0.4rem 0.8rem",
                        "borderRadius": "6px",
                        "cursor": "pointer",
                        "fontSize": "0.85rem",
                        "fontWeight": "500"
                    }
                },
                "Sair"
            )
        )
    )