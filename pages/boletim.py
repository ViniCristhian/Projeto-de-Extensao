from reactpy import component, html
from database.connection import ler_csv

@component
def PaginaBoletim(usuario_logado):
    aluno_id = usuario_logado.get("aluno_id", "1")
    notas = [n for n in ler_csv("notas") if n["aluno_id"] == aluno_id]
    disciplinas = {d["id"]: d["nome"] for d in ler_csv("disciplinas")}

    return html.div(
        {"style": {"padding": "20px"}},
        html.h2(f"Boletim do Aluno: {usuario_logado['nome']}"),
        html.table(
            {"style": {"width": "100%", "border-collapse": "collapse"}},
            html.thead(
                html.tr(
                    html.th({"style": {"border": "1px solid #ccc"}}, "Disciplina"),
                    html.th({"style": {"border": "1px solid #ccc"}}, "Período"),
                    html.th({"style": {"border": "1px solid #ccc"}}, "Nota")
                )
            ),
            html.tbody([
                html.tr(
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, disciplinas.get(n["disciplina_id"], "N/A")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, n["periodo"]),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, n["nota"])
                ) for n in notas
            ])
        )
    )