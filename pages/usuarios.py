from reactpy import component, html, hooks

from database.connection import exportar_csv, listar_filtrados, ler_csv, validar_usuario, escrever_csv, gerar_novo_id


@component
def PaginaUsuarios():
    usuarios, set_usuarios = hooks.use_state(ler_csv("usuarios"))
    alunos = ler_csv("alunos")
    termo_busca, set_termo_busca = hooks.use_state("")
    login, set_login = hooks.use_state("")
    senha, set_senha = hooks.use_state("")
    perfil, set_perfil = hooks.use_state("aluno")
    nome, set_nome = hooks.use_state("")
    aluno_id, set_aluno_id = hooks.use_state(alunos[0]["id"] if alunos else "")
    editando_id, set_editando_id = hooks.use_state(None)
    erro, set_erro = hooks.use_state("")
    mensagem_exportacao, set_mensagem_exportacao = hooks.use_state("")

    def limpar_formulario():
        set_login("")
        set_senha("")
        set_nome("")
        set_perfil("aluno")
        if alunos:
            set_aluno_id(alunos[0]["id"])
        set_editando_id(None)
        set_erro("")

    def salvar(event):
        dados = {
            "login": login,
            "senha": senha,
            "perfil": perfil,
            "nome": nome,
            "aluno_id": aluno_id if perfil == "aluno" else "",
        }
        valido, mensagem = validar_usuario(dados, editando_id)
        if not valido:
            set_erro(mensagem)
            return

        registros = list(usuarios)
        usuario_novo = {
            "id": str(editando_id) if editando_id is not None else str(gerar_novo_id("usuarios")),
            "login": login.strip(),
            "senha": senha.strip(),
            "perfil": perfil,
            "nome": nome.strip(),
            "aluno_id": aluno_id if perfil == "aluno" else "",
        }

        if editando_id is not None:
            registros = [
                usuario_novo if str(item.get("id")) == str(editando_id) else item
                for item in registros
            ]
        else:
            registros.append(usuario_novo)

        escrever_csv("usuarios", registros, ["id", "login", "senha", "perfil", "nome", "aluno_id"])
        set_usuarios(registros)
        limpar_formulario()

    def editar(usuario):
        set_editando_id(usuario.get("id"))
        set_login(usuario.get("login", ""))
        set_senha(usuario.get("senha", ""))
        set_perfil(usuario.get("perfil", "aluno"))
        set_nome(usuario.get("nome", ""))
        set_aluno_id(usuario.get("aluno_id", alunos[0]["id"] if alunos else ""))
        set_erro("")

    def excluir(usuario_id):
        registros = [item for item in usuarios if str(item.get("id")) != str(usuario_id)]
        escrever_csv("usuarios", registros, ["id", "login", "senha", "perfil", "nome", "aluno_id"])
        set_usuarios(registros)
        if editando_id == usuario_id:
            limpar_formulario()

    def exportar():
        caminho = exportar_csv("usuarios", usuarios, ["id", "login", "senha", "perfil", "nome", "aluno_id"], "usuarios_export.csv")
        set_mensagem_exportacao(f"Arquivo exportado em: {caminho}")

    lista_filtrada = listar_filtrados(usuarios, termo_busca, ["nome", "login", "perfil"])

    return html.div(
        {"style": {"padding": "20px", "display": "flex", "flexDirection": "column", "gap": "1.5rem"}},
        html.h2("Gerenciamento de Perfis"),
        html.div(
            {"style": {"border": "1px solid #ccc", "padding": "15px", "margin-bottom": "20px", "borderRadius": "8px", "background": "#fafafa"}},
            html.h3({"style": {"marginTop": "0"}}, "Novo Usuário"),
            html.p({"style": {"color": "#b91c1c", "minHeight": "1.2rem", "margin": "0 0 0.8rem 0"}}, erro),
            html.input({"placeholder": "Nome Completo", "value": nome, "on_change": lambda e: set_nome(e["target"]["value"]), "style": {"display": "block", "margin-bottom": "8px", "width": "100%"}}),
            html.input({"placeholder": "Login", "value": login, "on_change": lambda e: set_login(e["target"]["value"]), "style": {"display": "block", "margin-bottom": "8px", "width": "100%"}}),
            html.input({"type": "password", "placeholder": "Senha", "value": senha, "on_change": lambda e: set_senha(e["target"]["value"]), "style": {"display": "block", "margin-bottom": "8px", "width": "100%"}}),
            html.select({"value": perfil, "on_change": lambda e: set_perfil(e["target"]["value"]), "style": {"display": "block", "margin-bottom": "8px", "width": "100%"}}, html.option({"value": "administrador"}, "Administrador"), html.option({"value": "professor"}, "Professor"), html.option({"value": "aluno"}, "Aluno")),
            html.select({"value": aluno_id, "on_change": lambda e: set_aluno_id(e["target"]["value"]), "style": {"display": "block", "margin-bottom": "8px", "width": "100%"}} if perfil == "aluno" else {"style": {"display": "none"}} , [html.option({"value": a["id"]}, a["nome"]) for a in alunos] if alunos else []),
            html.button({"on_click": salvar, "style": {"padding": "0.6rem 1rem", "background": "#2563eb", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Salvar"),
        ),
        html.div(
            {"style": {"display": "flex", "justifyContent": "space-between", "alignItems": "center", "gap": "1rem", "flexWrap": "wrap"}},
            html.input({"placeholder": "Filtrar por nome, login ou perfil", "value": termo_busca, "on_change": lambda e: set_termo_busca(e["target"]["value"]), "style": {"flex": "1", "minWidth": "220px", "padding": "0.6rem"}}),
            html.button({"on_click": exportar, "style": {"padding": "0.6rem 1rem", "background": "#059669", "color": "white", "border": "none", "borderRadius": "6px", "cursor": "pointer"}}, "Exportar CSV")
        ),
        html.p({"style": {"color": "#047857", "margin": "0"}}, mensagem_exportacao),
        html.table(
            {"style": {"width": "100%", "borderCollapse": "collapse", "background": "white"}},
            html.thead(
                html.tr(
                    html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "ID"),
                    html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Nome"),
                    html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Login"),
                    html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Perfil"),
                    html.th({"style": {"border": "1px solid #ccc", "padding": "8px"}}, "Ações"),
                )
            ),
            html.tbody([
                html.tr(
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("id", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("nome", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("login", "")),
                    html.td({"style": {"border": "1px solid #ccc", "padding": "8px"}}, item.get("perfil", "")),
                    html.td(
                        {"style": {"border": "1px solid #ccc", "padding": "8px"}},
                        html.button({"on_click": lambda e, usuario=item: editar(usuario), "style": {"marginRight": "0.5rem", "padding": "0.4rem 0.7rem", "background": "#fbbf24", "color": "#111827", "border": "none", "borderRadius": "4px", "cursor": "pointer"}}, "Editar"),
                        html.button({"on_click": lambda e, usuario=item: excluir(usuario.get("id")), "style": {"padding": "0.4rem 0.7rem", "background": "#ef4444", "color": "white", "border": "none", "borderRadius": "4px", "cursor": "pointer"}}, "Excluir")
                    )
                ) for item in lista_filtrada
            ])
        )
    )