def incluir(conn, nome):
    cursor = conn.execute("INSERT INTO classes (nome) VALUES (?)", (nome,))
    conn.commit()
    return cursor.lastrowid


def buscar_por_id(conn, id):
    cursor = conn.execute("SELECT id, nome FROM classes WHERE id = ?", (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome):
    cursor = conn.execute(
        "SELECT id, nome FROM classes WHERE nome LIKE ? ORDER BY nome",
        ("%" + nome + "%",))
    return cursor.fetchall()


def listar(conn):
    cursor = conn.execute("SELECT id, nome FROM classes ORDER BY id")
    return cursor.fetchall()
