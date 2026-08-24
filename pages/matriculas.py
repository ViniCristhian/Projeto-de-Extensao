# pages/matriculas.py
from reactpy import component, html, hooks
from database.connection import BANCO_MEMORIA

@component
def PaginaMatriculas():
    # Estados locais baseados no banco em memória
    matriculas, set_matriculas = hooks.use_state(BANCO_MEMORIA["matriculas"])
    alunos = BANCO_MEMORIA["alunos"]
    turmas = BANCO_MEMORIA["turmas"]

    # Campos do formulário
    aluno_selecionado, set_aluno_selecionado = hooks.use_state(str(alunos[0]["id"]) if alunos else "")
    turma_selecionada, set_turma_selecionada = hooks.use_state(str(turmas[0]["id"]) if turmas else "")
    periodo, set_periodo = hooks.use_state("2026/1")

    def realizar_matricula(event):
        if aluno_selecionado and turma_selecionada:
            nova = {
                "id": len(matriculas) + 1,
                "aluno_id": int(aluno_selecionado),
                "turma_id": int(turma_selecionada),
                "periodo": periodo,
                "status": "Ativo"
            }
            # Atualiza memória global e estado local
            BANCO_MEMORIA["matriculas"].append(nova)
            set_matriculas(list(BANCO_MEMORIA["matriculas"]))

    # Função auxiliar para buscar nome do aluno pelo ID
    def obter_nome_aluno(aid):
        for a in alunos:
            if a["id"] == aid:
                return a["nome"]
        return "Desconhecido"

    # Função auxiliar para buscar nome da turma pelo ID
    def obter_nome_turma(tid):
        for t in turmas:
            if t["id"] == tid:
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
                        html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, obter_nome_turma(m["turma_id"])),
                        html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, m["periodo"]),
                        html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, m["status"]),
                    )
                    for m in matriculas
                ]
            )
        )
    )