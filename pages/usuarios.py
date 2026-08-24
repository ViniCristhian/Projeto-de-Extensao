from reactpy import component, html, hooks
from database.connection import ler_csv, salvar_csv

@component
def PaginaUsuarios():
    usuarios, set_usuarios = hooks.use_state(ler_csv("usuarios"))
    alunos = ler_csv("alunos")
    
    login, set_login = hooks.use_state("")
    senha, set_senha = hooks.use_state("")
    perfil, set_perfil = hooks.use_state("aluno")
    nome, set_nome = hooks.use_state("")
    aluno_id, set_aluno_id = hooks.use_state(alunos[0]["id"] if alunos else "")

    def cadastrar(e):
        if login and senha and nome:
            novos_dados = list(usuarios)
            novos_dados.append({
                "id": str(len(novos_dados) + 1),
                "login": login,
                "senha": senha,
                "perfil": perfil,
                "nome": nome,
                "aluno_id": aluno_id if perfil == "aluno" else ""
            })
            salvar_csv("usuarios", novos_dados)
            set_usuarios(novos_dados)
            set_login(""); set_senha(""); set_nome("")

    return html.div(
        {"style": {"padding": "20px"}},
        html.h2("Gerenciamento de Perfis"),
        html.div(
            {"style": {"border": "1px solid #ccc", "padding": "15px", "margin-bottom": "20px"}},
            html.h3("Novo Usuário"),
            html.input({"placeholder": "Nome Completo", "value": nome, "on_change": lambda e: set_nome(e["target"]["value"]), "style": {"display": "block", "margin-bottom": "8px"}}),
            html.input({"placeholder": "Login", "value": login, "on_change": lambda e: set_login(e["target"]["value"]), "style": {"display": "block", "margin-bottom": "8px"}}),
            html.input({"type": "password", "placeholder": "Senha", "value": senha, "on_change": lambda e: set_senha(e["target"]["value"]), "style": {"display": "block", "margin-bottom": "8px"}}),
            html.select(
                {"value": perfil, "on_change": lambda e: set_perfil(e["target"]["value"]), "style": {"display": "block", "margin-bottom": "8px"}},
                html.option({"value": "administrador"}, "Administrador"),
                html.option({"value": "professor"}, "Professor"),
                html.option({"value": "aluno"}, "Aluno")
            ),
            html.button({"on_click": cadastrar}, "Salvar no CSV")
        ),
        html.ul([html.li(f"{u['nome']} ({u['perfil']}) - Login: {u['login']}") for u in usuarios])
    )