from reactpy import component, html, hooks
from database.connection import ler_csv, salvar_csv

@component
def PaginaLancarNotas():
    notas, set_notas = hooks.use_state(ler_csv("notas"))
    alunos = ler_csv("alunos")
    disciplinas = ler_csv("disciplinas")

    aluno_id, set_aluno_id = hooks.use_state(alunos[0]["id"] if alunos else "")
    disciplina_id, set_disciplina_id = hooks.use_state(disciplinas[0]["id"] if disciplinas else "")
    valor_nota, set_valor_nota = hooks.use_state("")

    def salvar(e):
        if valor_nota:
            novas = list(notas)
            novas.append({
                "id": str(len(novas) + 1),
                "aluno_id": aluno_id,
                "disciplina_id": disciplina_id,
                "nota": valor_nota,
                "periodo": "2026/1"
            })
            salvar_csv("notas", novas)
            set_notas(novas)
            set_valor_nota("")

    return html.div(
        {"style": {"padding": "20px"}},
        html.h2("Lançamento de Notas (Professor/Admin)"),
        html.div(
            {"style": {"border": "1px solid #ccc", "padding": "15px", "margin-bottom": "20px"}},
            html.label("Aluno: "),
            html.select({"value": aluno_id, "on_change": lambda e: set_aluno_id(e["target"]["value"])},
                        [html.option({"value": a["id"]}, a["nome"]) for a in alunos]),
            html.br(), html.br(),
            html.label("Disciplina: "),
            html.select({"value": disciplina_id, "on_change": lambda e: set_disciplina_id(e["target"]["value"])},
                        [html.option({"value": d["id"]}, d["nome"]) for d in disciplinas]),
            html.br(), html.br(),
            html.input({"placeholder": "Nota (ex: 8.5)", "value": valor_nota, "on_change": lambda e: set_valor_nota(e["target"]["value"])}),
            html.button({"on_click": salvar, "style": {"margin-left": "10px"}}, "Registrar Nota")
        ),
        html.h3("Notas Cadastradas"),
        html.ul([html.li(f"Aluno ID: {n['aluno_id']} | Disciplina ID: {n['disciplina_id']} | Nota: {n['nota']}") for n in notas])
    )