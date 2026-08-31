from reactpy import component, html, hooks

from database.connection import exportar_csv, gerar_novo_id, listar_filtrados, ler_csv, escrever_csv


@component
def PaginaRequerimentos(usuario_logado):
    reqs, set_reqs = hooks.use_state(ler_csv("requerimentos"))
    tipo, set_tipo = hooks.use_state("Declaração de Matrícula")
    termo_busca, set_termo_busca = hooks.use_state("")
    erro, set_erro = hooks.use_state("")
    mensagem_exportacao, set_mensagem_exportacao = hooks.use_state("")

    def solicitar(e):
        aluno_id = usuario_logado.get("aluno_id", "")
        if not aluno_id:
            set_erro("Este usuário não está vinculado a um aluno.")
            return

        novos = list(reqs)
        novos.append({
            "id": str(gerar_novo_id("requerimentos")),
            "aluno_id": aluno_id,
            "tipo": tipo,
            "status": "Pendente",
        })
        escrever_csv("requerimentos", novos, ["id", "aluno_id", "tipo", "status"])
        set_reqs(novos)
        set_erro("")

    def alterar_status(item_id, novo_status):
        atualizados = []
        for item in reqs:
            if str(item.get("id")) == str(item_id):
                item = dict(item)
                item["status"] = novo_status
            atualizados.append(item)
        escrever_csv("requerimentos", atualizados, ["id", "aluno_id", "tipo", "status"])
        set_reqs(atualizados)

    def exportar():
        caminho = exportar_csv("requerimentos", reqs, ["id", "aluno_id", "tipo", "status"], "requerimentos_export.csv")
        set_mensagem_exportacao(f"Arquivo exportado em: {caminho}")

    lista_visivel = reqs if usuario_logado["perfil"] == "administrador" else [r for r in reqs if str(r.get("aluno_id", "")) == str(usuario_logado.get("aluno_id", ""))]
    lista_filtrada = listar_filtrados(lista_visivel, termo_busca, ["aluno_id", "tipo", "status"])

    return html.div({"style": {"padding": "20px", "display": "flex", "flexDirection": "column", "gap": "1.5rem"}},
        html.h2("Módulo de Requerimentos"),
        html.div({"style": {"margin-bottom": "20px", "border": "1px solid #ddd", "padding": "15px", "borderRadius": "8px", "background": "#fafafa"}},
            html.p({"style": {"color": "#b91c1c", "minHeight": "1.2rem", "margin": "0 0 0.8rem 0"}}, erro),
            html.select({"value": tipo, "on_change": lambda e: set_tipo(e["target"]["value"])},
                html.option({"value": "Declaração de Matrícula"}, "Declaração de Matrícula"),
                html.option({"value": "Histórico Escolar"}, "Histórico Escolar"),
                html.option({"value": "Revisão de Nota"}, "Revisão de Nota")),
            html.button({"on_click": solicitar, "style": {"marginLeft": "10px", "padding": "0.6rem 1rem", "background": "#2563eb", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Abrir Requerimento")),
        html.div({"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center", "gap": "1rem", "flexWrap": "wrap"}},
            html.input({"placeholder": "Filtrar por aluno, tipo ou status", "value": termo_busca, "on_change": lambda e: set_termo_busca(e["target"]["value"]), "style": {"flex": "1", "minWidth": "220px", "padding": "0.6rem"}}),
            html.button({"on_click": exportar, "style": {"padding": "0.6rem 1rem", "background": "#059669", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Exportar CSV")),
        html.p({"style": {"color": "#047857", "margin": "0"}}, mensagem_exportacao),
        html.h3("Solicitações"),
        html.table({"style": {"width": "100%", "borderCollapse": "collapse", "background": "white"}},
            html.thead(html.tr(html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "ID"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Aluno"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Tipo"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Status"), html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Ação"))),
            html.tbody([
                html.tr(
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("id", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("aluno_id", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("tipo", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("status", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, html.button({"on_click": lambda e, item=item: alterar_status(item.get("id"), "Aprovado"), "style": {"padding": "0.4rem 0.7rem", "background": "#16a34a", "color": "white", "border": "none", "borderRadius": "4px", "cursor": "pointer"}} if usuario_logado["perfil"] == "administrador" else {"display": "none"}, "Aprovar") if usuario_logado["perfil"] == "administrador" else "")
                ) for item in lista_filtrada
            ])
        )
    )