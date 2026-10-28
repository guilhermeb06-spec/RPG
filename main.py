import sqlite3

import banco
import classes
import jogadores
import itens
import personagens
import inventario

def ler_inteiro(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto.isdigit():
            return int(texto)
        print("  Digite um número inteiro.")


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto != "":
            return texto
        print("  Este campo não pode ficar vazio.")


def mostrar(colunas, linhas):
    if not linhas:
        print("  Nenhum registro encontrado.")
        return
    
    larguras = []
    for i, nome in enumerate(colunas):
        maior = max(len(str(linha[i])) for linha in linhas)
        larguras.append(max(len(nome), maior))
    print("  " + " | ".join(nome.ljust(l) for nome, l in zip(colunas, larguras)))
    print("  " + "-+-".join("-" * l for l in larguras))
    for linha in linhas:
        print("  " + " | ".join(str(v).ljust(l) for v, l in zip(linha, larguras)))

def dados_classe():
    nome = ler_texto("Nome da classe: ")
    return (nome,)


def dados_jogador():
    nome = ler_texto("Nome do jogador: ")
    apelido = input("Apelido (nick): ").strip()
    return (nome, apelido)


def dados_item():
    nome = ler_texto("Nome do item: ")
    tipo = input("Tipo (Arma, Poção, Armadura...): ").strip()
    poder = ler_inteiro("nivel de Poder (0 a 100): ")
    return (nome, tipo, poder)


def dados_personagem():
    nome = ler_texto("Nome do personagem: ")
    nivel = ler_inteiro("Nível (0 a 100): ")
    jogador_id = ler_texto("Id do jogador: ")
    classe_id = ler_inteiro("Id da classe: ")
    return (nome, nivel, jogador_id, classe_id)


def dados_inventario():
    personagem_id = ler_inteiro("Id do personagem: ")
    item_id = ler_inteiro("Id do item: ")
    quantidade = ler_inteiro("Quantidade: ")
    return (personagem_id, item_id, quantidade)

TABELAS = {
    "1": ("Classes",     classes,     ["Id", "Nome"],                                     dados_classe),
    "2": ("Jogadores",   jogadores,   ["Id", "Nome", "Apelido"],                          dados_jogador),
    "3": ("Itens",       itens,       ["Id", "Nome", "Tipo", "Poder"],                    dados_item),
    "4": ("Personagens", personagens, ["Id", "Nome", "Nível", "Jogador", "Classe"],       dados_personagem),
    "5": ("Inventário",  inventario,  ["Id", "Personagem", "Item", "Tipo", "Quantidade"], dados_inventario),
}


def submenu(conn, titulo, modulo, colunas, pedir_dados):
    while True:
        print(f"\n--- {titulo.upper()} ---")
        print("1 - Incluir")
        print("2 - Buscar por id")
        print("3 - Buscar por nome")
        print("4 - Listar todos")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        try:
            if opcao == "1":
                valores = pedir_dados()
                novo_id = modulo.incluir(conn, *valores)
                print(f"  Registro incluído com id {novo_id}.")
            elif opcao == "2":
                id = ler_inteiro("Id: ")
                linha = modulo.buscar_por_id(conn, id)
                if linha is None:
                    print("  Nenhum registro com esse id.")
                else:
                    mostrar(colunas, [linha])
            elif opcao == "3":
                texto = ler_texto("Nome (ou parte dele): ")
                mostrar(colunas, modulo.buscar_por_nome(conn, texto))
            elif opcao == "4":
                mostrar(colunas, modulo.listar(conn))
            elif opcao == "0":
                return
            else:
                print("  Opção inválida.")
        except NotImplementedError:
            print("  Esta função ainda não foi implementada. Abra o arquivo "
                  f"{modulo.__name__}.py e complete o código.")
        except sqlite3.IntegrityError as erro:
            print(f"  O banco recusou a operação: {erro}")
            print("  (Confira se os ids informados existem.)")


def main():
    conn = banco.conectar()
    print("Conectado ao banco:", banco.NOME_ARQUIVO)

    while True:
        print("\n===== RPG - CADASTRO DO JOGO =====")
        for chave, (titulo, *_) in TABELAS.items():
            print(f"{chave} - {titulo}")
        print("6 - Carregar dados de exemplo")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao in TABELAS:
            titulo, modulo, colunas, pedir_dados = TABELAS[opcao]
            submenu(conn, titulo, modulo, colunas, pedir_dados)
        elif opcao == "6":
            if banco.carregar_exemplos(conn):
                print("  Dados de exemplo carregados.")
            else:
                print("  O banco já tem dados; nada foi alterado.")
        elif opcao == "0":
            break
        else:
            print("  Opção inválida.")

    conn.close()
    print("Até logo!")


if __name__ == "__main__":
    main()
