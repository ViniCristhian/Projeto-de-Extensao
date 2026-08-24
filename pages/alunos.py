from reactpy import component, html, hooks
from database.connection import BANCO_MEMORIA

@component
def PaginaAlunos():
    alunos, set_alunos = hooks.use_state(BANCO_MEMORIA["alunos"])
    nome, set_nome = hooks.use_state("")
    cpf, set_cpf = hooks.use_state("")

    def salvar(e):
        if nome:
            novo = {"id": len(alunos) + 1, "nome": nome, "cpf": cpf, "turma_atual": "Não Enturmado"}
            BANCO_MEMORIA["alunos"].append(novo)
            set_alunos(list(BANCO_MEMORIA["alunos"]))
            set_nome(""); set_cpf("")

    return html.div(
        {"style": {"padding": "20px"}},
        html.h2("Gestão de Alunos"),
        html.div(
            {"style": {"border": "1px solid #ddd", "padding": "15px", "margin-bottom": "20px"}},
            html.input({"placeholder": "Nome do Aluno", "value": nome, "on_change": lambda e: set_nome(e["target"]["value"])}),
            html.input({"placeholder": "CPF", "value": cpf, "on_change": lambda e: set_cpf(e["target"]["value"])}),
            html.button({"on_click": salvar}, "Cadastrar Aluno")
        ),
        html.table(
            {"style": {"width": "100%", "text-align": "left"}},
            html.thead(html.tr(html.th("ID"), html.th("Nome"), html.th("CPF"), html.th("Status"))),
            html.tbody([html.tr(html.td(a["id"]), html.td(a["nome"]), html.td(a["cpf"]), html.td(a["turma_atual"])) for a in alunos])
        )
    )
# Nota: páginas `professores.py` e `disciplinas.py` usam exatamente a mesma lógica estrutural, alterando apenas os campos (ex: especialidade em vez de CPF).