from reactpy import html
from database.connection import ler_csv


def dashboard(usuario_logado, navegar):
    usuarios = ler_csv("usuarios")
    alunos = ler_csv("alunos")
    disciplinas = ler_csv("disciplinas")
    notas = ler_csv("notas")
    requerimentos = ler_csv("requerimentos")
    perfil = usuario_logado.get("perfil", "aluno")

    def formatar_numero(valor):
        return f"{valor:,}".replace(",", ".") if isinstance(valor, int) else str(valor)

    if perfil == "administrador":
        cards_metricas = [
            {"titulo": "Usuários Cadastrados", "valor": formatar_numero(len(usuarios)), "cor": "#2563eb"},
            {"titulo": "Alunos Registrados", "valor": formatar_numero(len(alunos)), "cor": "#059669"},
            {"titulo": "Disciplinas Ativas", "valor": formatar_numero(len(disciplinas)), "cor": "#7c3aed"},
            {"titulo": "Requerimentos Pendentes", "valor": formatar_numero(sum(1 for r in requerimentos if r.get("status") == "Pendente")), "cor": "#d97706"},
        ]
        atalhos = [
            ("usuarios", "👤 Gestão de Perfis"),
            ("notas", "📝 Lançar Notas"),
            ("requerimentos", "📨 Requerimentos"),
        ]
    elif perfil == "professor":
        cards_metricas = [
            {"titulo": "Disciplinas sob sua responsabilidade", "valor": formatar_numero(len(disciplinas)), "cor": "#2563eb"},
            {"titulo": "Notas Lançadas", "valor": formatar_numero(len(notas)), "cor": "#059669"},
            {"titulo": "Alunos Cadastrados", "valor": formatar_numero(len(alunos)), "cor": "#7c3aed"},
            {"titulo": "Requerimentos Pendentes", "valor": formatar_numero(sum(1 for r in requerimentos if r.get("status") == "Pendente")), "cor": "#d97706"},
        ]
        atalhos = [
            ("notas", "📝 Lançar Notas"),
            ("requerimentos", "📨 Ver Requerimentos"),
        ]
    elif perfil == "aluno":
        aluno_id = usuario_logado.get("aluno_id", "1")
        notas_aluno = [float(n.get("nota", 0)) for n in notas if str(n.get("aluno_id")) == str(aluno_id)]
        media = sum(notas_aluno) / len(notas_aluno) if notas_aluno else 0
        cards_metricas = [
            {"titulo": "Minha Média", "valor": f"{media:.1f}", "cor": "#2563eb"},
            {"titulo": "Requerimentos", "valor": formatar_numero(sum(1 for r in requerimentos if str(r.get("aluno_id")) == str(aluno_id))), "cor": "#059669"},
            {"titulo": "Notas Registradas", "valor": formatar_numero(len(notas_aluno)), "cor": "#7c3aed"},
            {"titulo": "Disciplinas", "valor": formatar_numero(len(disciplinas)), "cor": "#d97706"},
        ]
        atalhos = [
            ("boletim", "📄 Meu Boletim"),
            ("requerimentos", "📨 Solicitar Requerimento"),
        ]
    else:
        cards_metricas = [
            {"titulo": "Registros", "valor": formatar_numero(len(usuarios)), "cor": "#2563eb"},
            {"titulo": "Pendentes", "valor": formatar_numero(sum(1 for r in requerimentos if r.get("status") == "Pendente")), "cor": "#d97706"},
        ]
        atalhos = [("home", "🏠 Início")]

    return html.div(
        {"style": {"display": "flex", "flexDirection": "column", "gap": "2rem"}},
        html.div(
            html.h2({"style": {"fontSize": "1.8rem", "margin": "0 0 0.5rem 0", "color": "#0f172a"}}, "Painel Principal"),
            html.p({"style": {"color": "#64748b", "margin": "0"}}, f"Bem-vindo(a), {usuario_logado.get('nome', 'Usuário')}! Aqui estão os indicadores do sistema para seu perfil.")
        ),
        html.div(
            {"style": {"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(220px, 1fr))", "gap": "1.5rem"}},
            [
                html.div(
                    {
                        "key": item["titulo"],
                        "style": {
                            "background": "#ffffff",
                            "padding": "1.5rem",
                            "borderRadius": "8px",
                            "borderLeft": f"5px solid {item['cor']}",
                            "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.1)"
                        }
                    },
                    html.span({"style": {"color": "#64748b", "fontSize": "0.875rem"}}, item["titulo"]),
                    html.h3({"style": {"fontSize": "1.8rem", "margin": "0.5rem 0 0 0", "color": "#0f172a"}}, item["valor"])
                ) for item in cards_metricas
            ]
        ),
        html.div(
            {"style": {"background": "#ffffff", "padding": "1.5rem", "borderRadius": "8px", "boxShadow": "0 1px 3px rgba(0, 0, 0, 0.1)"}},
            html.h3({"style": {"fontSize": "1.2rem", "marginTop": "0", "marginBottom": "1rem"}}, "Ações Rápidas"),
            html.div(
                {"style": {"display": "flex", "gap": "1rem", "flexWrap": "wrap"}},
                [
                    html.button(
                        {
                            "key": rota,
                            "on_click": lambda e, destino=rota: navegar(destino),
                            "style": {"padding": "0.7rem 1.2rem", "background": "#2563eb", "color": "#fff", "border": "none", "borderRadius": "6px", "cursor": "pointer"}
                        },
                        nome
                    ) for rota, nome in atalhos
                ]
            )
        )
    )