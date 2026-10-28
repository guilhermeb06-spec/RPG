def incluir(conn, nome, apelido):
    cursor = conn.execute(
        "INSERT INTO jogadores (nome, apelido) VALUES (?, ?)", (nome, apelido))
    conn.commit()
    return cursor.lastrowid


def buscar_por_id(conn, id):
    cursor = conn.execute(
        "SELECT id, nome, apelido FROM jogadores WHERE id = ?", (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome):
    cursor = conn.execute(
        "SELECT id, nome, apelido FROM jogadores WHERE nome LIKE ? ORDER BY nome",
        ("%" + nome + "%",))
    return cursor.fetchall()


def listar(conn):
    cursor = conn.execute(
        "SELECT id, nome, apelido FROM jogadores ORDER BY id")
    return cursor.fetchall()
