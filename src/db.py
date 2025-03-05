import logging
import mysql.connector
from mysql.connector import Error

def connect_db():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
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
