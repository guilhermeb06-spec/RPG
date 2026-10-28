CONSULTA = """
    SELECT personagens.id, personagens.nome, personagens.nivel,
           jogadores.apelido, classes.nome
    FROM personagens
    JOIN jogadores ON jogadores.id = personagens.jogador_id
    JOIN classes ON classes.id = personagens.classe_id
"""
def incluir(conn, nome, nivel, jogador_id, classe_id):
    cursor = conn.execute(
        "INSERT INTO personagens (nome, nivel, jogador_id, classe_id) "
        "VALUES (?, ?, ?, ?)", (nome, nivel, jogador_id, classe_id))
    conn.commit()
    return cursor.lastrowid


def buscar_por_id(conn, id):
    cursor = conn.execute(CONSULTA + " WHERE personagens.id = ?", (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome):
    cursor = conn.execute(
        CONSULTA + " WHERE personagens.nome LIKE ? ORDER BY personagens.nome",
        ("%" + nome + "%",))
    return cursor.fetchall()


def listar(conn):
    cursor = conn.execute(CONSULTA + " ORDER BY personagens.id")
    return cursor.fetchall()
