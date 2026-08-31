from reactpy import component, html, hooks

from database.connection import exportar_csv, gerar_novo_id, listar_filtrados, ler_csv, escrever_csv


@component
def PaginaProfessores():
    professores, set_professores = hooks.use_state(ler_csv("professores"))
    termo_busca, set_termo_busca = hooks.use_state("")
    nome, set_nome = hooks.use_state("")
    disciplina, set_disciplina = hooks.use_state("")
    editando_id, set_editando_id = hooks.use_state(None)
    erro, set_erro = hooks.use_state("")
    mensagem_exportacao, set_mensagem_exportacao = hooks.use_state("")

    def limpar_formulario():
        set_nome("")
        set_disciplina("")
        set_editando_id(None)
        set_erro("")

    def salvar(event):
        nome_limpo = nome.strip()
        disciplina_limpa = disciplina.strip()
        if not nome_limpo:
            set_erro("Informe o nome do professor.")
            return
        if not disciplina_limpa:
            set_erro("Informe a disciplina do professor.")
            return

        registros = list(professores)
        dados = {
            "id": str(editando_id) if editando_id is not None else str(gerar_novo_id("professores")),
            "nome": nome_limpo,
            "disciplina": disciplina_limpa,
        }

        if editando_id is not None:
            registros = [dados if str(item.get("id")) == str(editando_id) else item for item in registros]
        else:
            registros.append(dados)

        escrever_csv("professores", registros, ["id", "nome", "disciplina"])
        set_professores(registros)
        limpar_formulario()

    def editar(item):
        set_editando_id(item.get("id"))
        set_nome(item.get("nome", ""))
        set_disciplina(item.get("disciplina", ""))
        set_erro("")

    def excluir(item_id):
        registros = [item for item in professores if str(item.get("id")) != str(item_id)]
        escrever_csv("professores", registros, ["id", "nome", "disciplina"])
        set_professores(registros)
        if editando_id == item_id:
            limpar_formulario()

    def exportar():
        caminho = exportar_csv("professores", professores, ["id", "nome", "disciplina"], "professores_export.csv")
        set_mensagem_exportacao(f"Arquivo exportado em: {caminho}")

    lista_filtrada = listar_filtrados(professores, termo_busca, ["nome", "disciplina"])

    return html.div(
        {"style": {"padding": "20px", "display": "flex", "flexDirection": "column", "gap": "1.5rem"}},
        html.h2("Professores"),
        html.div({"style": {"border": "1px solid #ddd", "padding": "15px", "borderRadius": "8px", "background": "#fafafa"}},
            html.h3({"style": {"marginTop": "0"}}, "Cadastrar / Editar Professor"),
            html.p({"style": {"color": "#b91c1c", "minHeight": "1.2rem", "margin": "0 0 0.8rem 0"}}, erro),
            html.input({"placeholder": "Nome do professor", "value": nome, "on_change": lambda e: set_nome(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}),
            html.input({"placeholder": "Disciplina", "value": disciplina, "on_change": lambda e: set_disciplina(e["target"]["value"]), "style": {"display": "block", "marginBottom": "8px", "width": "100%"}}),
            html.button({"on_click": salvar, "style": {"padding": "0.6rem 1rem", "background": "#2563eb", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Salvar")),
        html.div({"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center", "gap": "1rem", "flexWrap": "wrap"}},
            html.input({"placeholder": "Filtrar por nome ou disciplina", "value": termo_busca, "on_change": lambda e: set_termo_busca(e["target"]["value"]), "style": {"flex": "1", "minWidth": "220px", "padding": "0.6rem"}}),
            html.button({"on_click": exportar, "style": {"padding": "0.6rem 1rem", "background": "#059669", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Exportar CSV")),
        html.p({"style": {"color": "#047857", "margin": "0"}}, mensagem_exportacao),
        html.table({"style": {"width": "100%", "borderCollapse": "collapse", "background": "white"}},
            html.thead(html.tr(html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "ID"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Nome"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Disciplina"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Ações"))),
            html.tbody([
                html.tr(
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("id", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("nome", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("disciplina", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, html.button({"on_click": lambda e, professor=item: editar(professor), "style": {"marginRight": "0.5rem", "padding": "0.4rem 0.7rem", "background": "#fbbf24", "color": "#111827", "border": "none", "borderRadius": "4px", "cursor": "pointer"}}, "Editar"), html.button({"on_click": lambda e, professor=item: excluir(professor.get("id")), "style": {"padding": "0.4rem 0.7rem", "background": "#ef4444", "color": "white", "border": "none", "borderRadius": "4px", "cursor": "pointer"}}, "Excluir"))
                ) for item in lista_filtrada
            ])
        )
    )