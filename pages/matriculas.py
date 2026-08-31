from reactpy import component, html, hooks

from database.connection import exportar_csv, gerar_novo_id, listar_filtrados, ler_csv, escrever_csv


@component
def PaginaMatriculas():
    matriculas, set_matriculas = hooks.use_state(ler_csv("matriculas"))
    alunos = ler_csv("alunos")
    turmas = ler_csv("turmas")
    termo_busca, set_termo_busca = hooks.use_state("")

    aluno_selecionado, set_aluno_selecionado = hooks.use_state(str(alunos[0]["id"]) if alunos else "")
    turma_selecionada, set_turma_selecionada = hooks.use_state(str(turmas[0]["id"]) if turmas else "")
    periodo, set_periodo = hooks.use_state("2026/1")
    status, set_status = hooks.use_state("Ativo")
    editando_id, set_editando_id = hooks.use_state(None)
    erro, set_erro = hooks.use_state("")
    mensagem_exportacao, set_mensagem_exportacao = hooks.use_state("")

    def limpar_formulario():
        if alunos:
            set_aluno_selecionado(str(alunos[0]["id"]))
        if turmas:
            set_turma_selecionada(str(turmas[0]["id"]))
        set_periodo("2026/1")
        set_status("Ativo")
        set_editando_id(None)
        set_erro("")

    def salvar(event):
        if not aluno_selecionado or not turma_selecionada:
            set_erro("Selecione um aluno e uma turma.")
            return

        registros = list(matriculas)
        dados = {
            "matricula": str(editando_id) if editando_id is not None else str(gerar_novo_id("matriculas")),
            "turma": str(turma_selecionada),
            "periodo": periodo or "2026/1",
            "status": status,
        }

        if editando_id is not None:
            registros = [dados if str(item.get("id")) == str(editando_id) else item for item in registros]
        else:
            registros.append(dados)

        escrever_csv("matriculas", registros, ["id", "aluno_id", "turma", "periodo", "status"])
        set_matriculas(registros)
        limpar_formulario()

    def editar(item):
        set_editando_id(item.get("id"))
        set_aluno_selecionado(str(item.get("aluno_id", "")))
        set_turma_selecionada(str(item.get("turma", "")))
        set_periodo(item.get("periodo", "2026/1"))
        set_status(item.get("status", "Ativo"))
        set_erro("")

    def excluir(item_id):
        registros = [item for item in matriculas if str(item.get("id")) != str(item_id)]
        escrever_csv("matriculas", registros, ["id", "aluno_id", "turma", "periodo", "status"])
        set_matriculas(registros)
        if editando_id == item_id:
            limpar_formulario()

    def obter_nome_aluno(aid):
        for aluno in alunos:
            if str(aluno.get("id")) == str(aid):
                return aluno.get("nome", "")
        return "Desconhecido"

    def obter_nome_turma(tid):
        for turma in turmas:
            if str(turma.get("id")) == str(tid):
                return turma.get("nome", "")
        return "Desconhecida"

    def exportar():
        caminho = exportar_csv("matriculas", matriculas, ["id", "aluno_id", "turma", "periodo", "status"], "matriculas_export.csv")
        set_mensagem_exportacao(f"Arquivo exportado em: {caminho}")

    lista_filtrada = listar_filtrados(matriculas, termo_busca, ["aluno_id", "turma", "periodo", "status"])

    return html.div({"style": {"padding": "20px", "display": "flex", "flexDirection": "column", "gap": "1.5rem"}},
        html.h2("Matrículas e Enturmação"),
        html.div({"style": {"border": "1px solid #ddd", "padding": "15px", "borderRadius": "8px", "background": "#fafafa"}},
            html.h3({"style": {"marginTop": "0"}}, "Efetuar matrícula"),
            html.p({"style": {"color": "#b91c1c", "minHeight": "1.2rem", "margin": "0 0 0.8rem 0"}}, erro),
            html.select({"value": aluno_selecionado, "on_change": lambda e: set_aluno_selecionado(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}, [html.option({"value": str(aluno["id"])}, aluno["nome"]) for aluno in alunos]),
            html.select({"value": turma_selecionada, "on_change": lambda e: set_turma_selecionada(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}, [html.option({"value": str(turma["id"])}, f"{turma['nome']} ({turma.get('serie', '')})") for turma in turmas]),
            html.input({"placeholder": "Período acadêmico", "value": periodo, "on_change": lambda e: set_periodo(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}),
            html.select({"value": status, "on_change": lambda e: set_status(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}, html.option({"value": "Ativo"}, "Ativo"), html.option({"value": "Inativo"}, "Inativo")),
            html.button({"on_click": salvar, "style": {"padding": "0.6rem 1rem", "background": "#2563eb", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Salvar")),
        html.div({"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center", "gap": "1rem", "flexWrap": "wrap"}},
            html.input({"placeholder": "Filtrar por aluno, turma, período ou status", "value": termo_busca, "on_change": lambda e: set_termo_busca(e["target"]["value"]), "style": {"flex": "1", "minWidth": "220px", "padding": "0.6rem"}}),
            html.button({"on_click": exportar, "style": {"padding": "0.6rem 1rem", "background": "#059669", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Exportar CSV")),
        html.p({"style": {"color": "#047857", "margin": "0"}}, mensagem_exportacao),
        html.table({"style": {"width": "100%", "borderCollapse": "collapse", "background": "white"}},
            html.thead(html.tr(html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "ID"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Aluno"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Turma"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Período"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Status"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Ações"))),
            html.tbody([
                html.tr(
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("id", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, obter_nome_aluno(item.get("aluno_id", ""))),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, obter_nome_turma(item.get("turma", ""))),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("periodo", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("status", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, html.button({"on_click": lambda e, matricula=item: editar(matricula), "style": {"marginRight": "0.5rem", "padding": "0.4rem 0.7rem", "background": "#fbbf24", "color": "#111827", "border": "none", "borderRadius": "4px", "cursor": "pointer"}}, "Editar"), html.button({"on_click": lambda e, matricula=item: excluir(matricula.get("id")), "style": {"padding": "0.4rem 0.7rem", "background": "#ef4444", "color": "white", "border": "none", "borderRadius": "4px", "cursor": "pointer"}}, "Excluir"))
                ) for item in lista_filtrada
            ])
        )
    )