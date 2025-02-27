from .db import connection_test
import customtkinter as ctk

def test_database_connection():
    """Executa o teste de conexão com o banco e retorna a mensagem correspondente."""
    return connection_test()


def boas_vindas(frame):
    import customtkinter as ctk

def boas_vindas(frame):
    # Frame para os rótulos de boas-vindas
    welcome_frame = ctk.CTkFrame(frame, fg_color="white")

    # Função para renderizar a mensagem de boas-vindas
    label_line1 = ctk.CTkLabel(welcome_frame, text="Seja bem-vindo ao app", font=("Helvetica", 16))
    label_line1.pack(pady=(20, 0))

    label_line2= ctk.CTkLabel(welcome_frame, text="Gerenciador de Dispensa", font=("Helvetica", 22, "bold"))
    label_line2.pack(pady=(10, 0))

    label_line3 = ctk.CTkLabel(welcome_frame, text="Selecione a opção que deseja utilizar", font=("Helvetica", 16))
    label_line3.pack(pady=(10, 20))

    welcome_frame.pack(expand=True)
    return welcome_frame
