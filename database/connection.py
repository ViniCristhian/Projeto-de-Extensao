import csv
import os

DATA_DIR = os.path.dirname(__file__)

ESQUEMAS = {
    "usuarios": {
        "cols": ["id", "login", "senha", "perfil", "nome", "aluno_id"],
        "inicial": [
            {"id": "1", "login": "admin", "senha": "123", "perfil": "administrador", "nome": "Admin Principal", "aluno_id": ""},
            {"id": "2", "login": "roberto", "senha": "123", "perfil": "professor", "nome": "Prof. Roberto", "aluno_id": ""},
            {"id": "3", "login": "ana", "senha": "123", "perfil": "aluno", "nome": "Ana Souza", "aluno_id": "1"},
        ],
    },
    "alunos": {
        "cols": ["id", "nome", "cpf", "turma_atual"],
        "inicial": [{"id": "1", "nome": "Ana Souza", "cpf": "111.111.111-11", "turma_atual": "101"}],
    },
    "professores": {
        "cols": ["id", "nome", "disciplina"],
        "inicial": [{"id": "1", "nome": "Prof. Roberto", "disciplina": "Matemática"}],
    },
    "disciplinas": {
        "cols": ["id", "nome", "professor_id"],
        "inicial": [{"id": "1", "nome": "Matemática", "professor_id": "1"}],
    },
    "turmas": {
        "cols": ["id", "nome", "serie", "turno"],
        "inicial": [{"id": "1", "nome": "101", "serie": "1º ano", "turno": "Manhã"}],
    },
    "matriculas": {
        "cols": ["id", "aluno_id", "turma", "periodo", "status"],
        "inicial": [{"id": "1", "aluno_id": "1", "turma": "1", "periodo": "2026/1", "status": "Ativo"}],
    },
    "notas": {
        "cols": ["id", "aluno_id", "disciplina_id", "nota", "periodo"],
        "inicial": [{"id": "1", "aluno_id": "1", "disciplina_id": "1", "nota": "9.5", "periodo": "2026/1"}],
    },
    "requerimentos": {
        "cols": ["id", "aluno_id", "tipo", "status"],
        "inicial": [{"id": "1", "aluno_id": "1", "tipo": "Declaração de Matrícula", "status": "Pendente"}],
    },
}


def escrever_csv(nome_tabela: str, dados: list[dict], colunas: list[str] | None = None):
    os.makedirs(DATA_DIR, exist_ok=True)
    caminho = os.path.join(DATA_DIR, f"{nome_tabela}.csv")
    campos = colunas or ESQUEMAS.get(nome_tabela, {}).get("cols", [])

    with open(caminho, mode="w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        if dados:
            escritor.writerows(dados)


def inicializar_csvs() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    for nome_tabela, config in ESQUEMAS.items():
        caminho = os.path.join(DATA_DIR, f"{nome_tabela}.csv")
        if os.path.exists(caminho):
            continue
        escrever_csv(nome_tabela, config["inicial"], config["cols"])


inicializar_csvs()


def ler_csv(nome_tabela: str) -> list[dict]:
    caminho = os.path.join(DATA_DIR, f"{nome_tabela}.csv")
    if not os.path.exists(caminho):
        return []

    with open(caminho, mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)
        if not leitor.fieldnames:
            return []
        return [dict(linha) for linha in leitor]


def listar_filtrados(registros: list[dict], termo: str, campos: list[str]) -> list[dict]:
    busca = (termo or "").strip().lower()
    if not busca:
        return list(registros)

    resultado = []
    for registro in registros:
        valores = [str(registro.get(campo, "")).lower() for campo in campos if campo in registro]
        if any(busca in valor for valor in valores):
            resultado.append(registro)
    return resultado


def exportar_csv(nome_tabela: str, dados: list[dict] | None = None, colunas: list[str] | None = None, nome_arquivo: str | None = None) -> str:
    registros = dados if dados is not None else ler_csv(nome_tabela)
    campos = colunas or ESQUEMAS.get(nome_tabela, {}).get("cols", [])
    pasta_exportacao = os.path.join(DATA_DIR, "relatorios")
    os.makedirs(pasta_exportacao, exist_ok=True)
    nome = nome_arquivo or f"{nome_tabela}_export.csv"
    caminho = os.path.join(pasta_exportacao, nome)

    with open(caminho, mode="w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        if registros:
            escritor.writerows(registros)
    return caminho


def gerar_novo_id(nome_tabela: str) -> int:
    registros = ler_csv(nome_tabela)
    ids = []
    for registro in registros:
        valor = registro.get("id")
        if valor is None:
            continue
        try:
            ids.append(int(str(valor).strip()))
        except ValueError:
            continue
    return max(ids, default=0) + 1


def validar_usuario(usuario: dict, usuario_id_excluir: str | None = None) -> tuple[bool, str]:
    login = (usuario.get("login") or "").strip()
    senha = (usuario.get("senha") or "").strip()
    nome = (usuario.get("nome") or "").strip()
    perfil = (usuario.get("perfil") or "").strip()

    if not nome:
        return False, "Informe o nome completo do usuário."
    if len(login) < 3:
        return False, "O login deve conter pelo menos 3 caracteres."
    if len(senha) < 3:
        return False, "A senha deve conter pelo menos 3 caracteres."
    if perfil not in ["administrador", "professor", "aluno"]:
        return False, "Selecione um perfil válido."

    for existente in ler_csv("usuarios"):
        if str(existente.get("id")) == str(usuario_id_excluir):
            continue
        if (existente.get("login") or "").strip().lower() == login.lower():
            return False, "Já existe um usuário com esse login."

    return True, ""


def validar_nota(valor: str) -> tuple[bool, str]:
    texto = (valor or "").strip().replace(",", ".")
    if not texto:
        return False, "Informe a nota do aluno."
    try:
        nota = float(texto)
    except ValueError:
        return False, "A nota deve ser numérica, como 8.5."
    if nota < 0 or nota > 10:
        return False, "A nota deve estar entre 0 e 10."
    return True, ""


def autenticar_usuario(login: str, senha: str) -> dict | None:
    usuarios = ler_csv("usuarios")
    login_digitado = (login or "").strip().lower()
    senha_digitada = (senha or "").strip()

    for usuario in usuarios:
        if (usuario.get("login") or "").strip().lower() == login_digitado and (usuario.get("senha") or "").strip() == senha_digitada:
            return usuario
    return None