import mysql.connector #Importa o módulo mysql.connector para conectar ao banco de dados MySQL
from mysql.connector import Error ## Importa a classe Error para tratar exceções relacionadas ao MySQL

def connection_test():
    # Tenta estabelecer uma conexão com o banco de dados MySQL usando os parâmetros fornecidos
    db = None #inicia a variavel db
    try:
        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "dispensa"
        )

        if db.is_connected(): #verifica se a conexão foi bem-sucedida
            return "✅ Conexão bem-sucedida com o banco de dados 'dispensa'."
        
        return "⚠️ A conexão falhou por um motivo desconhecido."
        
    except Error as err: #captura qualquer exceção gerada durante o processo de conexão
        return f"❌ Erro ao conectar ao banco de dados: {err}" #retorna a mensagem com o erro
    
    finally:
        if db and db.is_connected():
            db.close()  # Fecha a conexão apenas se estiver ativa

