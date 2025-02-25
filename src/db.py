import mysql.connector #Importa o módulo mysql.connector para conectar ao banco de dados MySQL
from mysql.connector import Error ## Importa a classe Error para tratar exceções relacionadas ao MySQL

def connection_test():
    # Tenta estabelecer uma conexão com o banco de dados MySQL usando os parâmetros fornecidos
    try:
        db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "dispensa"
        )

        if db.is_connected(): #verifica se a conexão foi bem-sucedida
            return "A conexão com o banco de dados foi bem-sucedida."
        db.close() #fecha a conexão com o bando de dados
    except Error as err: #capitura qualquer exceção gerada durante o processo de conexão
        return f"Erro: {err}" #retorna a mensagem com o erro
