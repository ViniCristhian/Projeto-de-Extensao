# pages/matriculas.py
#Comentario de teste para commit
from reactpy import component, html, hooks
from database.connection import ler_csv, escrever_csv

@component
def PaginaMatriculas():
    matriculas, set_matriculas = hooks.use_state(ler_csv("matriculas"))
    alunos = ler_csv("alunos")
    turmas = ler_csv("turmas")

    aluno_selecionado, set_aluno_selecionado = hooks.use_state(str(alunos[0]["id"]) if alunos else "")
    turma_selecionada, set_turma_selecionada = hooks.use_state(str(turmas[0]["id"]) if turmas else "")
    periodo, set_periodo = hooks.use_state("2026/1")

    def realizar_matricula(event):
        if aluno_selecionado and turma_selecionada:
            nova = {
                "id": str(len(matriculas) + 1),
                "aluno_id": str(aluno_selecionado),
                "turma": str(turma_selecionada),
                "periodo": periodo,
                "status": "Ativo"
            }
            novos_dados = list(matriculas)
            novos_dados.append(nova)
            escrever_csv("matriculas", novos_dados, ["id", "aluno_id", "turma", "periodo", "status"])
            set_matriculas(novos_dados)

    def obter_nome_aluno(aid):
        for a in alunos:
            if str(a["id"]) == str(aid):
                return a["nome"]
        return "Desconhecido"

    def obter_nome_turma(tid):
        for t in turmas:
            if str(t["id"]) == str(tid):
                return t["nome"]
        return "Desconhecida"

    return html.div(
        {"style": {"padding": "20px"}},
        html.h2("Módulo de Matrículas e Enturmação"),
        
        # Formulário de Nova Matrícula
        html.div(
            {"style": {"border": "1px solid #ddd", "padding": "15px", "margin-bottom": "20px", "background": "#fafafa"}},
            html.h3("Efetuar Nova Matrícula"),
            html.div(
                {"style": {"margin-bottom": "10px"}},
                html.label({"style": {"display": "block"}}, "Aluno:"),
                html.select(
                    {
                        "value": aluno_selecionado,
                        "on_change": lambda e: set_aluno_selecionado(e["target"]["value"])
                    },
                    [html.option({"value": str(a["id"])}, a["nome"]) for a in alunos]
                )
            ),
            html.div(
                {"style": {"margin-bottom": "10px"}},
                html.label({"style": {"display": "block"}}, "Turma:"),
                html.select(
                    {
                        "value": turma_selecionada,
                        "on_change": lambda e: set_turma_selecionada(e["target"]["value"])
                    },
                    [html.option({"value": str(t["id"])}, f"{t['nome']} ({t['serie']})") for t in turmas]
                )
            ),
            html.div(
                {"style": {"margin-bottom": "10px"}},
                html.label({"style": {"display": "block"}}, "Período Acadêmico:"),
                html.input({
                    "type": "text",
                    "value": periodo,
                    "on_change": lambda e: set_periodo(e["target"]["value"])
                })
            ),
            html.button({"on_click": realizar_matricula}, "Matrícula Aluno")
        ),

        # Listagem de Matrículas Ativas
        html.h3("Matrículas Registradas"),
        html.table(
            {"style": {"width": "100%", "border-collapse": "collapse"}},
            html.thead(
                html.tr(
                    html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "ID"),
                    html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Aluno"),
                    html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Turma"),
                    html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Período"),
                    html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Status"),
                )
            ),
            html.tbody(
                [
                    html.tr(
                        html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, str(m["id"])),
                        html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, obter_nome_aluno(m["aluno_id"])),
                        html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, obter_nome_turma(m.get("turma_id", m.get("turma", "")))),
                        html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, m["periodo"]),
                        html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, m["status"]),
                    )
                    for m in matriculas
                ]
            )
        )
    )