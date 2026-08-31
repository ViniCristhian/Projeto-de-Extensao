from reactpy import component, html, hooks

from database.connection import exportar_csv, gerar_novo_id, listar_filtrados, ler_csv, escrever_csv


@component
def PaginaAlunos():
    alunos, set_alunos = hooks.use_state(ler_csv("alunos"))
    termo_busca, set_termo_busca = hooks.use_state("")
    nome, set_nome = hooks.use_state("")
    cpf, set_cpf = hooks.use_state("")
    turma_atual, set_turma_atual = hooks.use_state("")
    editando_id, set_editando_id = hooks.use_state(None)
    erro, set_erro = hooks.use_state("")
    mensagem_exportacao, set_mensagem_exportacao = hooks.use_state("")

    def limpar_formulario():
        set_nome("")
        set_cpf("")
        set_turma_atual("")
        set_editando_id(None)
        set_erro("")

    def salvar(event):
        nome_limpo = nome.strip()
        cpf_limpo = cpf.strip()
        turma = turma_atual.strip() or "Não Enturmado"
        if not nome_limpo:
            set_erro("Informe o nome do aluno.")
            return
        if not cpf_limpo:
            set_erro("Informe o CPF do aluno.")
            return

        registros = list(alunos)
        dados = {
            "id": str(editando_id) if editando_id is not None else str(gerar_novo_id("alunos")),
            "nome": nome_limpo,
            "cpf": cpf_limpo,
            "turma_atual": turma,
        }

        if editando_id is not None:
            registros = [dados if str(item.get("id")) == str(editando_id) else item for item in registros]
        else:
            registros.append(dados)

        escrever_csv("alunos", registros, ["id", "nome", "cpf", "turma_atual"])
        set_alunos(registros)
        limpar_formulario()

    def editar(item):
        set_editando_id(item.get("id"))
        set_nome(item.get("nome", ""))
        set_cpf(item.get("cpf", ""))
        set_turma_atual(item.get("turma_atual", ""))
        set_erro("")

    def excluir(item_id):
        registros = [item for item in alunos if str(item.get("id")) != str(item_id)]
        escrever_csv("alunos", registros, ["id", "nome", "cpf", "turma_atual"])
        set_alunos(registros)
        if editando_id == item_id:
            limpar_formulario()

    def exportar():
        caminho = exportar_csv("alunos", alunos, ["id", "nome", "cpf", "turma_atual"], "alunos_export.csv")
        set_mensagem_exportacao(f"Arquivo exportado em: {caminho}")

    lista_filtrada = listar_filtrados(alunos, termo_busca, ["nome", "cpf", "turma_atual"])

    return html.div(
        {"style": {"padding": "20px", "display": "flex", "flexDirection": "column", "gap": "1.5rem"}},
        html.h2("Gestão de Alunos"),
        html.div(
            {"style": {"border": "1px solid #ddd", "padding": "15px", "borderRadius": "8px", "background": "#fafafa"}},
            html.h3({"style": {"marginTop": "0"}}, "Cadastrar / Editar Aluno"),
            html.p({"style": {"color": "#b91c1c", "minHeight": "1.2rem", "margin": "0 0 0.8rem 0"}}, erro),
            html.input({"placeholder": "Nome do aluno", "value": nome, "on_change": lambda e: set_nome(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}),
            html.input({"placeholder": "CPF", "value": cpf, "on_change": lambda e: set_cpf(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}),
            html.input({"placeholder": "Turma atual", "value": turma_atual, "on_change": lambda e: set_turma_atual(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}),
            html.button({"on_click": salvar, "style": {"padding": "0.6rem 1rem", "background": "#2563eb", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Salvar"),
        ),
        html.div({"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center", "gap": "1rem", "flexWrap": "wrap"}},
            html.input({"placeholder": "Filtrar por nome, CPF ou turma", "value": termo_busca, "on_change": lambda e: set_termo_busca(e["target"]["value"]), "style": {"flex": "1", "minWidth": "220px", "padding": "0.6rem"}}),
            html.button({"on_click": exportar, "style": {"padding": "0.6rem 1rem", "background": "#059669", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Exportar CSV")),
        html.p({"style": {"color": "#047857", "margin": "0"}}, mensagem_exportacao),
        html.table({"style": {"width": "100%", "borderCollapse": "collapse", "background": "white"}},
            html.thead(html.tr(html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "ID"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Nome"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "CPF"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Turma"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Ações"))),
            html.tbody([
                html.tr(
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("id", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("nome", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("cpf", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("turma_atual", "Não Enturmado")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, html.button({"on_click": lambda e, aluno=item: editar(aluno), "style": {"marginRight": "0.5rem", "padding": "0.4rem 0.7rem", "background": "#fbbf24", "color": "#111827", "border": "none", "borderRadius": "4px", "cursor": "pointer"}}, "Editar"), html.button({"on_click": lambda e, aluno=item: excluir(aluno.get("id")), "style": {"padding": "0.4rem 0.7rem", "background": "#ef4444", "color": "white", "border": "none", "borderRadius": "4px", "cursor": "pointer"}}, "Excluir"))
                ) for item in lista_filtrada
            ])
        )
    )