from reactpy import component, html, hooks
from database.connection import ler_csv, escrever_csv

@component
def PaginaRequerimentos(usuario_logado):
    reqs, set_reqs = hooks.use_state(ler_csv("requerimentos"))
    tipo, set_tipo = hooks.use_state("Declaração de Matrícula")

    def solicitar(e):
        novos = list(reqs)
        novos.append({
            "id": str(len(novos) + 1),
            "aluno_id": usuario_logado.get("aluno_id", "1"),
            "tipo": tipo,
            "status": "Pendente"
        })
        escrever_csv("requerimentos", novos, ["id", "aluno_id", "tipo", "status"])
        set_reqs(novos)

    lista_visivel = reqs if usuario_logado["perfil"] == "administrador" else [r for r in reqs if r["aluno_id"] == usuario_logado.get("aluno_id")]

    return html.div(
        {"style": {"padding": "20px"}},
        html.h2("Módulo de Requerimentos"),
        html.div(
            {"style": {"margin-bottom": "20px"}},
            html.select({"value": tipo, "on_change": lambda e: set_tipo(e["target"]["value"])},
                        html.option({"value": "Declaração de Matrícula"}, "Declaração de Matrícula"),
                        html.option({"value": "Histórico Escolar"}, "Histórico Escolar"),
                        html.option({"value": "Revisão de Nota"}, "Revisão de Nota")),
            html.button({"on_click": solicitar, "style": {"margin-left": "10px"}}, "Abrir Requerimento")
        ),
        html.h3("Solicitações"),
        html.ul([html.li(f"ID {r['id']} | Tipo: {r['tipo']} | Status: {r['status']}") for r in lista_visivel])
    )