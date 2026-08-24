import csv
import os

DATA_DIR = os.path.dirname(__file__)

# Esquemas de colunas e dados iniciais padrão
ESQUEMAS = {
    "usuarios": {
        "cols": ["id", "login", "senha", "perfil", "nome", "aluno_id"],
        "inicial": [
            {"id": "1", "login": "admin", "senha": "123", "perfil": "administrador", "nome": "Admin Principal", "aluno_id": ""},
            {"id": "2", "login": "roberto", "senha": "123", "perfil": "professor", "nome": "Prof. Roberto", "aluno_id": ""},
            {"id": "3", "login": "ana", "senha": "123", "perfil": "aluno", "nome": "Ana Souza", "aluno_id": "1"}
        ]
    },
    "alunos": {
        "cols": ["id", "nome", "cpf"],
        "inicial": [{"id": "1", "nome": "Ana Souza", "cpf": "111.111.111-11"}]
    },
    "professores": {
        "cols": ["id", "nome", "disciplina"],
        "inicial": [{"id": "1", "nome": "Prof. Roberto", "disciplina": "Matemática"}]
    },
    "disciplinas": {
        "cols": ["id", "nome", "professor_id"],
        "inicial": [{"id": "1", "nome": "Matemática", "professor_id": "1"}]
    },
    "matriculas": {
        "cols": ["id", "aluno_id", "turma", "periodo", "status"],
        "inicial": [{"id": "1", "aluno_id": "1", "turma": "101", "periodo": "2026/1", "status": "Ativo"}]
    },
    "notas": {
        "cols": ["id", "aluno_id", "disciplina_id", "nota", "periodo"],
        "inicial": [{"id": "1", "aluno_id": "1", "disciplina_id": "1", "nota": "9.5", "periodo": "2026/1"}]
    },
    "requerimentos": {
        "cols": ["id", "aluno_id", "tipo", "status"],
        "inicial": [{"id": "1", "aluno_id": "1", "tipo": "Declaração de Matrícula", "status": "Pendente"}]
    }
}

def ler_csv(tabela):
    caminho = os.path.join(DATA_DIR, f"{tabela}.csv")
    esquema = ESQUEMAS[tabela]
    
    if not os.path.exists(caminho):
        salvar_csv(tabela, esquema["inicial"])
        return esquema["inicial"]
    
    with open(caminho, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def salvar_csv(tabela, dados):
    caminho = os.path.join(DATA_DIR, f"{tabela}.csv")
    cols = ESQUEMAS[tabela]["cols"]
    
    with open(caminho, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader()
        writer.writerows(dados)