from reactpy import component, html, hooks

from database.connection import exportar_csv, gerar_novo_id, listar_filtrados, ler_csv, escrever_csv


@component
def PaginaDisciplinas():
    disciplinas, set_disciplinas = hooks.use_state(ler_csv("disciplinas"))
    professores = ler_csv("professores")
    termo_busca, set_termo_busca = hooks.use_state("")
    nome, set_nome = hooks.use_state("")
    professor_id, set_professor_id = hooks.use_state(professores[0]["id"] if professores else "")
    editando_id, set_editando_id = hooks.use_state(None)
    erro, set_erro = hooks.use_state("")
    mensagem_exportacao, set_mensagem_exportacao = hooks.use_state("")

    def limpar_formulario():
        set_nome("")
        if professores:
            set_professor_id(professores[0]["id"])
        set_editando_id(None)
        set_erro("")

    def salvar(event):
        nome_limpo = nome.strip()
        if not nome_limpo:
            set_erro("Informe o nome da disciplina.")
            return

        registros = list(disciplinas)
        dados = {
            "id": str(editando_id) if editando_id is not None else str(gerar_novo_id("disciplinas")),
            "nome": nome_limpo,
            "professor_id": professor_id,
        }

        if editando_id is not None:
            registros = [dados if str(item.get("id")) == str(editando_id) else item for item in registros]
        else:
            registros.append(dados)

        escrever_csv("disciplinas", registros, ["id", "nome", "professor_id"])
        set_disciplinas(registros)
        limpar_formulario()

    def editar(item):
        set_editando_id(item.get("id"))
        set_nome(item.get("nome", ""))
        set_professor_id(item.get("professor_id", professores[0]["id"] if professores else ""))
        set_erro("")

    def excluir(item_id):
        registros = [item for item in disciplinas if str(item.get("id")) != str(item_id)]
        escrever_csv("disciplinas", registros, ["id", "nome", "professor_id"])
        set_disciplinas(registros)
        if editando_id == item_id:
            limpar_formulario()

    def nome_professor(pid):
        for professor in professores:
            if str(professor.get("id")) == str(pid):
                return professor.get("nome", "")
        return "Não informado"

    def exportar():
        caminho = exportar_csv("disciplinas", disciplinas, ["id", "nome", "professor_id"], "disciplinas_export.csv")
        set_mensagem_exportacao(f"Arquivo exportado em: {caminho}")

    lista_filtrada = listar_filtrados(disciplinas, termo_busca, ["nome", "professor_id"])

    return html.div({"style": {"padding": "20px", "display": "flex", "flexDirection": "column", "gap": "1.5rem"}},
        html.h2("Disciplinas"),
        html.div({"style": {"border": "1px solid #ddd", "padding": "15px", "borderRadius": "8px", "background": "#fafafa"}},
            html.h3({"style": {"marginTop": "0"}}, "Cadastrar / Editar Disciplina"),
            html.p({"style": {"color": "#b91c1c", "minHeight": "1.2rem", "margin": "0 0 0.8rem 0"}}, erro),
            html.input({"placeholder": "Nome da disciplina", "value": nome, "on_change": lambda e: set_nome(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}),
            html.select({"value": professor_id, "on_change": lambda e: set_professor_id(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}, [html.option({"value": str(p["id"])}, p.get("nome", "")) for p in professores] if professores else []),
            html.button({"on_click": salvar, "style": {"padding": "0.6rem 1rem", "background": "#2563eb", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Salvar")),
        html.div({"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center", "gap": "1rem", "flexWrap": "wrap"}},
            html.input({"placeholder": "Filtrar por nome ou professor", "value": termo_busca, "on_change": lambda e: set_termo_busca(e["target"]["value"]), "style": {"flex": "1", "minWidth": "220px", "padding": "0.6rem"}}),
            html.button({"on_click": exportar, "style": {"padding": "0.6rem 1rem", "background": "#059669", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Exportar CSV")),
        html.p({"style": {"color": "#047857", "margin": "0"}}, mensagem_exportacao),
        html.table({"style": {"width": "100%", "borderCollapse": "collapse", "background": "white"}},
            html.thead(html.tr(html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "ID"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Nome"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Professor"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Ações"))),
            html.tbody([
                html.tr(
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("id", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("nome", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, nome_professor(item.get("professor_id", ""))),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, html.button({"on_click": lambda e, disciplina=item: editar(disciplina), "style": {"marginRight": "0.5rem", "padding": "0.4rem 0.7rem", "background": "#fbbf24", "color": "#111827", "border": "none", "borderRadius": "4px", "cursor": "pointer"}}, "Editar"), html.button({"on_click": lambda e, disciplina=item: excluir(disciplina.get("id")), "style": {"padding": "0.4rem 0.7rem", "background": "#ef4444", "color": "white", "border": "none", "borderRadius": "4px", "cursor": "pointer"}}, "Excluir"))
                ) for item in lista_filtrada
            ])
        )
    )