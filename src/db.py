import logging
import mysql.connector
from mysql.connector import Error


def connect_db():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password='',
            database="dispensa"
        )
    except Error as err:
        logging.error(f"❌ Erro ao conectar ao banco de dados: {err}")
        return None


def connection_test():
    """Testa a conexão com o banco de dados."""
    db = connect_db()
    if db:
        db.close()
        logging.info("✅ Conexão bem-sucedida com o banco de dados 'dispensa'.")
        return True
    logging.error("❌ Falha ao conectar ao banco de dados.")
    return False


def execute_query(query, params=None, fetch=False):
    """Executa uma consulta SQL genérica."""
    db = connect_db()
    if not db:
        return None if fetch else {"status": False, "mensagem": "Falha na conexão com o banco de dados."}
    
    try:
        cursor = db.cursor(dictionary=True) if fetch else db.cursor()
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result
        
        db.commit()
        cursor.close()
        db.close()
        return {"status": True}
    except Error as err:
        logging.error(f"❌ Erro ao executar query: {err}")
        return None if fetch else {"status": False, "mensagem": str(err)}
    

def find_item_in_db(item_name, fields):
    """Encontra um item no banco de dados pelo nome."""
    query = f'SELECT {", ".join(fields)} FROM produtos WHERE nome = %s'
    result = execute_query(query, params=(item_name,), fetch=True)
    if result:
        return {"status": True, "item": result[0]}
    else:
        return {"status": False, "mensagem": "Item não encontrado."}


def get_items_from_db(fields):
    """Busca os itens do banco de dados."""
    query = f'SELECT {", ".join(fields)} FROM produtos ORDER BY nome ASC'
    result = execute_query(query, fetch=True)
    return result if result is not None else "❌ Erro ao buscar itens no banco de dados."


def add_item_to_db(values):
    """Adiciona um item ao banco de dados."""
    if not connection_test():
        return {"status": False, "mensagem": "Falha na conexão com o banco de dados."}
    
    nome, quantidade, quantidade_referencia, essencial, periodo = (
        values["nome"], values["quantidade"], values["quantidade_referencia"], values["essencial"], values["periodo"]
    )
    
    if execute_query("SELECT COUNT(*) FROM produtos WHERE nome = %s", (nome,), fetch=True)[0]['COUNT(*)'] > 0:
        logging.warning(f"⚠️ O Produto '{nome}' já existe no banco de dados.")
        return {"status": False, "mensagem": f"O Produto '{nome}' já existe!"}
    
    query = """
        INSERT INTO produtos (nome, quantidade, target, essencial, periodo_de_compra)
        VALUES (%s, %s, %s, %s, %s)
    """
    result = execute_query(query, (nome, quantidade, quantidade_referencia, essencial, periodo))
    
    if result["status"]:
        logging.info(f"✅ O Produto '{nome}' foi adicionado ao banco de dados com sucesso!")
    return result


def delete_item_from_db(item_name):
    """Remove um item do banco de dados."""
    if not connection_test():
        return {"status": False, "mensagem": "Falha na conexão com o banco de dados."}

    # Executar a query para remover o item pelo nome
    query = "DELETE FROM produtos WHERE nome = %s"
    result = execute_query(query, (item_name,))
    
    if result:
        logging.info(f"✅ O Produto '{item_name}' foi removido do banco de dados com sucesso!")
        return {"status": True, "mensagem": f"O Produto '{item_name}' foi removido com sucesso!"}
    else:
        logging.error(f"❌ Falha ao remover o Produto '{item_name}'.")
        return {"status": False, "mensagem": f"Falha ao remover o Produto '{item_name}'."}


def edit_quantity_in_db(items):
    logging.info('Atualizando quantidade no Banco de dados.')
    atualizar_quantidades = []
    for item in items:
        if item['quantidade'] != '':
            atualizar_quantidades.append({'nome': item['nome'], 'quantidade': item['quantidade']})

            query = "UPDATE produtos SET quantidade =  %s WHERE nome = %s"

            result = execute_query(query, params=(item['quantidade'], item['nome']))

            if result is not None and result.get('status'):
                logging.info(f'O produto {item["nome"]} foi atualizado para a quantidade {item["quantidade"]}.')
            else:
                mensagem = result.get("mensagem") if result is not None else "Erro desconhecido"
                logging.error(f"Erro ao atualizar o produto '{item['nome']}': {mensagem}")


def edit_item_in_db(item_name, query_list):
    """Edita um item no banco de dados com os valores fornecidos."""
    logging.info(f'Editando item "{item_name}" no banco de dados.')

    if not connection_test():
        return {"status": False, "mensagem": "Falha na conexão com o banco de dados."}

    if not query_list:
        logging.info(f"Nenhuma alteração identificada para o item: {item_name}")
        return {"status": True, "mensagem": "Nenhuma alteração necessária."}

    db = connect_db()
    cursor = db.cursor()

    try:
        set_clause = ", ".join([f"{campo} = %s" for campo in query_list.keys()])
        update_query = f"UPDATE produtos SET {set_clause} WHERE nome = %s"

        values = list(query_list.values()) + [item_name]
        cursor.execute(update_query, values)
        
        if cursor.rowcount > 0:
            db.commit()
            logging.info(f"Item '{item_name}' atualizado com sucesso: {query_list}")
            return {"status": True, "mensagem": "Item atualizado com sucesso."}
        else:
            logging.warning(f"Nenhum item atualizado. O nome '{item_name}' pode não existir.")
            return {"status": False, "mensagem": "Nenhuma alteração feita. O item pode não existir."}
    
    except Exception as e:
        db.rollback()
        logging.error(f"Erro ao atualizar o item '{item_name}': {e}")
        return {"status": False, "mensagem": "Erro ao atualizar o item no banco de dados."}

    finally:
        cursor.close()
        db.close()

def create_database_if_not_exists():
    """Cria o banco de dados 'dispensa' e a tabela 'produtos' se ainda não existirem."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS dispensa")
        connection.database = "dispensa"

        create_table_query = """
        CREATE TABLE IF NOT EXISTS produtos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL UNIQUE,
            quantidade INT NOT NULL,
            target INT NOT NULL,
            essencial BOOLEAN DEFAULT FALSE,
            periodo_de_compra VARCHAR(20)
        )
        """
        cursor.execute(create_table_query)
        connection.commit()
        logging.info("✅ Banco de dados e tabela criados.")
        return {"status": True, "mensagem": "Banco de dados criado com sucesso."}
    except Error as err:
        logging.error(f"Erro ao criar banco de dados: {err}")
        return {"status": False, "mensagem": f"Erro: {err}"}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
