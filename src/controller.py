from .db import connection_test
import customtkinter as ctk
import logging

def test_database_connection():
    """Executa o teste de conexão com o banco e retorna a mensagem correspondente."""
    return connection_test()


def show_results(label_result):
    """Atualiza o label de resultado com o status da conexão."""
    logging.info("Botão clicado! Tentando conexão...")
    try:
        result = test_database_connection()
        label_result.configure(text=result)
        logging.info("Resultado da conexão: %s", result)
    except Exception as e:
        logging.error("Erro ao tentar conexão", exc_info=True)



def boas_vindas(frame):
    """Cria a tela de boas-vindas."""
    welcome_frame = ctk.CTkFrame(frame, fg_color="white")

    labels = [
        ("Seja bem-vindo ao app", 16),
        ("Gerenciador de Dispensa", 22, "bold"),
        ("Selecione a opção que deseja utilizar", 16)
    ]

    for idx, (text, size, *style) in enumerate(labels):
        label = ctk.CTkLabel(welcome_frame, text=text, font=("Helvetica", size, *style))
        label.pack(pady=(20 if idx == 0 else 10, 0))

    welcome_frame.pack(expand=True)
    return welcome_frame


