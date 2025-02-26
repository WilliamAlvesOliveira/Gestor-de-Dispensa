from .db import connection_test

def test_database_connection():
    """Executa o teste de conexão com o banco e retorna a mensagem correspondente."""
    return connection_test()

