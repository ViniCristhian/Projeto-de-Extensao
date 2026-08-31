from reactpy import component, html, hooks

from database.connection import exportar_csv, gerar_novo_id, listar_filtrados, ler_csv, validar_nota, escrever_csv


@component
def PaginaLancarNotas():
    notas, set_notas = hooks.use_state(ler_csv("notas"))
    alunos = ler_csv("alunos")
    disciplinas = ler_csv("disciplinas")
    termo_busca, set_termo_busca = hooks.use_state("")

    aluno_id, set_aluno_id = hooks.use_state(alunos[0]["id"] if alunos else "")
    disciplina_id, set_disciplina_id = hooks.use_state(disciplinas[0]["id"] if disciplinas else "")
    valor_nota, set_valor_nota = hooks.use_state("")
    erro, set_erro = hooks.use_state("")
    mensagem_exportacao, set_mensagem_exportacao = hooks.use_state("")

    def salvar(e):
        valido, mensagem = validar_nota(valor_nota)
        if not valido:
            set_erro(mensagem)
            return
        if not aluno_id or not disciplina_id:
            set_erro("Selecione um aluno e uma disciplina.")
            return

        novas = list(notas)
        novas.append({
            "id": str(gerar_novo_id("notas")),
            "aluno_id": aluno_id,
            "disciplina_id": disciplina_id,
            "nota": str(float(valor_nota.replace(",", "."))),
            "periodo": "2026/1",
        })
        escrever_csv("notas", novas, ["id", "aluno_id", "disciplina_id", "nota", "periodo"])
        set_notas(novas)
        set_valor_nota("")
        set_erro("")

    def exportar():
        caminho = exportar_csv("notas", notas, ["id", "aluno_id", "disciplina_id", "nota", "periodo"], "notas_export.csv")
        set_mensagem_exportacao(f"Arquivo exportado em: {caminho}")

    lista_filtrada = listar_filtrados(notas, termo_busca, ["aluno_id", "disciplina_id", "nota", "periodo"])

    return html.div({"style": {"padding": "20px", "display": "flex", "flexDirection": "column", "gap": "1.5rem"}},
        html.h2("Lançamento de Notas (Professor/Admin)"),
        html.div({"style": {"border": "1px solid #ccc", "padding": "15px", "borderRadius": "8px", "background": "#fafafa"}},
            html.p({"style": {"color": "#b91c1c", "minHeight": "1.2rem", "margin": "0 0 0.8rem 0"}}, erro),
            html.label("Aluno: "),
            html.select({"value": aluno_id, "on_change": lambda e: set_aluno_id(e["target"]["value"])}, [html.option({"value": a["id"]}, a["nome"]) for a in alunos]),
            html.br(), html.br(),
            html.label("Disciplina: "),
            html.select({"value": disciplina_id, "on_change": lambda e: set_disciplina_id(e["target"]["value"])}, [html.option({"value": d["id"]}, d["nome"]) for d in disciplinas]),
            html.br(), html.br(),
            html.input({"placeholder": "Nota (ex: 8.5)", "value": valor_nota, "on_change": lambda e: set_valor_nota(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}),
            html.button({"on_click": salvar, "style": {"padding": "0.6rem 1rem", "background": "#2563eb", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Registrar Nota")),
        html.div({"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center", "gap": "1rem", "flexWrap": "wrap"}},
            html.input({"placeholder": "Filtrar por aluno, disciplina, nota ou período", "value": termo_busca, "on_change": lambda e: set_termo_busca(e["target"]["value"]), "style": {"flex": "1", "minWidth": "220px", "padding": "0.6rem"}}),
            html.button({"on_click": exportar, "style": {"padding": "0.6rem 1rem", "background": "#059669", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Exportar CSV")),
        html.p({"style": {"color": "#047857", "margin": "0"}}, mensagem_exportacao),
        html.h3("Notas Cadastradas"),
        html.ul([html.li(f"Aluno ID: {n['aluno_id']} | Disciplina ID: {n['disciplina_id']} | Nota: {n['nota']}") for n in lista_filtrada])
    )