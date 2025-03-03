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
        return False

# Função para buscar itens da tabela 'produtos'
def get_items_from_db():
    """Busca os itens do banco de dados e retorna uma lista de dicionários"""
    db = connect_db()
    if not db:  # Se a conexão falhou, retorna mensagem de erro
        return "❌ Infelizmente não conseguimos acessar os dados.\nClique em 'Testar Conexão' para verificar a conexão com o banco de dados."

    try:
        logging.info("✅ Conexão bem-sucedida com o banco de dados 'dispensa'.")
        cursor = db.cursor(dictionary=True)  # Retorna resultados como dicionário
        cursor.execute('SELECT nome, quantidade, target FROM produtos')
        items = cursor.fetchall()
        cursor.close()

        if items is None:  # Garante que sempre retorna uma lista
            return []

        return items  

    except Error as err:
        logging.error(f"❌ Erro ao buscar itens do banco de dados: {err}")
        return "❌ Erro ao buscar itens no banco de dados. Tente novamente mais tarde."

    finally:
        if db.is_connected():
            db.close()  # Fecha a conexão


# função para adicionar itens ao banco de dados
def add_item_to_db(values):
    """Adiciona um item ao banco de dados."""
    if not connection_test():
        return {"status": False, "mensagem": "Falha na conexão com o banco de dados."}

    nome = values["nome"]
    quantidade = values["quantidade"]
    quantidade_referencia = values["quantidade_referencia"]
    essencial = values["essencial"]
    periodo = values["periodo"]

    try:
        db = connect_db()
        if not db:
            return {"status": False, "mensagem": "Falha ao conectar ao banco de dados para inserção."}
        
        cursor = db.cursor()

        # Verifica se o produto já existe
        cursor.execute("SELECT COUNT(*) FROM produtos WHERE nome = %s", (nome,))
        if cursor.fetchone()[0] > 0:
            logging.warning(f"O Produto '{nome}' já existe no banco de dados.")
            return {"status": False, "mensagem": f"O Produto '{nome}' já existe!"}

        # Exemplo de comando SQL para adicionar um item
        sql_query = """
        INSERT INTO produtos (nome, quantidade, target, essencial, periodo_de_compra)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_query, (nome, quantidade, quantidade_referencia, essencial, periodo))

        db.commit()  # Confirma a transação
        logging.info(f"O Produto '{nome}' foi adicionado ao banco de dados com sucesso!")
        
        cursor.close()
        db.close()
        
        return {"status": True, "mensagem": f"O Produto '{nome}' foi adicionado ao banco de dados com sucesso!"}

    except Error as e:
        logging.error(f"Erro ao adicionar o Produto '{nome}' ao banco de dados: {e}")
        return {"status": False, "mensagem": f"Erro ao adicionar o Produto '{nome}' ao banco de dados: {e}"}

