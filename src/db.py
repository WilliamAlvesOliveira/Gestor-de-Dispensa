import logging
import mysql.connector
from mysql.connector import Error

# Função genérica para conectar ao banco de dados
def connect_db():
    """Cria e retorna uma conexão com o banco de dados"""
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dispensa"
        )
        return db
    except Error as err:
        logging.error(f"❌ Erro ao conectar ao banco de dados: {err}")
        return None  # Retorna None em caso de falha na conexão


# Função para testar a conexão com o banco
def connection_test():
    """Testa a conexão com o banco de dados"""
    try:
        db = connect_db()
        if db:
            db.close()
            logging.info("✅ Conexão bem-sucedida com o banco de dados 'dispensa'.")
            return True
        else:
            return False
    except Exception as e:
        logging.exception(f"❌ Exceção durante a tentativa de conexão ao banco de dados: {e}")
        return
    

# Função para buscar itens da tabela 'produtos'
def get_items_from_db():
    """Busca os itens do banco de dados e retorna uma lista de dicionários"""
    db = connect_db()
    if not db:  # Se a conexão falhou, retorna lista vazia
        return "❌ Infelizmente não conseguimos acessar os dados.\nClique em 'Testar Conexão' para verificar a conexão com o banco de dados."

    try:
        logging.info("✅ Conexão bem-sucedida com o banco de dados 'dispensa'.")
        cursor = db.cursor(dictionary=True)  # Retorna resultados como dicionário
        cursor.execute('SELECT nome, quantidade, target FROM produtos')
        items = cursor.fetchall()
        cursor.close()
        return items  # Retorna diretamente a lista de dicionários

    except Error as err:
        logging.error(f"❌ Erro ao buscar itens do banco de dados: {err}")
        return []

    finally:
        if db.is_connected():
            db.close()  # Fecha a conexão
