def incluir(conn, nome, tipo, poder):
    cursor = conn.execute(
        "INSERT INTO itens (nome, tipo, poder) VALUES (?, ?, ?)",
        (nome, tipo, poder))
    conn.commit()
    return cursor.lastrowid


def buscar_por_id(conn, id):
    cursor = conn.execute(
        "SELECT id, nome, tipo, poder FROM itens WHERE id = ?", (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome):
    cursor = conn.execute(
        "SELECT id, nome, tipo, poder FROM itens WHERE nome LIKE ? ORDER BY nome",
        ("%" + nome + "%",))
    return cursor.fetchall()


def listar(conn):
    cursor = conn.execute(
        "SELECT id, nome, tipo, poder FROM itens ORDER BY id")
    return cursor.fetchall()
