CONSULTA = """
    SELECT inventario.id, personagens.nome, itens.nome, itens.tipo,
           inventario.quantidade
    FROM inventario
    JOIN personagens ON personagens.id = inventario.personagem_id
    JOIN itens ON itens.id = inventario.item_id
"""


def incluir(conn, personagem_id, item_id, quantidade):
    cursor = conn.execute(
        "INSERT INTO inventario (personagem_id, item_id, quantidade) "
        "VALUES (?, ?, ?)", (personagem_id, item_id, quantidade))
    conn.commit()
    return cursor.lastrowid


def buscar_por_id(conn, id):
    cursor = conn.execute(CONSULTA + " WHERE inventario.id = ?", (id,))
    return cursor.fetchone()


def buscar_por_nome(conn, nome_personagem):
    cursor = conn.execute(
        CONSULTA + " WHERE personagens.nome LIKE ? ORDER BY personagens.nome",
        ("%" + nome_personagem + "%",))
    return cursor.fetchall()


def listar(conn):
    cursor = conn.execute(CONSULTA + " ORDER BY inventario.id")
    return cursor.fetchall()
