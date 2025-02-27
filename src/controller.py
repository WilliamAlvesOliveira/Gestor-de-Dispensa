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
        ("Gerenciador de Dispensa", 26, "bold"),
        ("Selecione a opção que deseja utilizar", 16)
    ]

    for idx, (text, size, *style) in enumerate(labels):
        label = ctk.CTkLabel(welcome_frame, text=text, font=("Helvetica", size, *style))
        label.pack(pady=(20 if idx == 0 else 10, 0))

    welcome_frame.pack(expand=True)
    return welcome_frame


def add_item_frame(frame):
    """Cria o frame para adicionar items"""
    # Limpa o frame
    for widget in frame.winfo_children():
        widget.destroy()  # Remove todos os widgets atuais do frame

    # Cria o novo frame
    add_frame = ctk.CTkFrame(frame, fg_color="white")
    add_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Adiciona o texto 'Adicionar Item' alinhado à esquerda
    label = ctk.CTkLabel(add_frame, text="Adicionar Item", anchor="w")  # 'w' para alinha à esquerda
    label.pack(fill="x", padx=5, pady=0)
    
    return add_frame


def remove_item_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy() # remove todos os widgets

    remove_frame = ctk.CTkFrame(frame, fg_color="white")
    remove_frame.pack(fill="both", expand=True, padx=10, pady=10)

    label = ctk.CTkLabel(remove_frame, text="Remover Item", anchor="w")
    label.pack(fill="x", padx=5, pady=0)

    return remove_frame


def edit_item_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    edit_frame = ctk.CTkFrame(frame, fg_color="white")
    edit_frame.pack(fill="both", expand=True, padx=10, pady=10)

    label = ctk.CTkLabel(edit_frame, text="Editar Item", anchor="w")
    label.pack(fill="x", padx=5, pady=0)

    return edit_frame


def show_list_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    show_list = ctk.CTkFrame(frame, fg_color="white")
    show_list.pack(fill="both", expand=True, padx=10, pady=10)

    label = ctk.CTkLabel(show_list, text="Items da Dispensa", anchor="w")
    label.pack(fill="x", padx=5, pady=0)


def shop_list_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    shop_list = ctk.CTkFrame(frame, fg_color="white")
    shop_list.pack(fill="both", expand=True, padx=10, pady=10)

    label = ctk.CTkLabel(shop_list, text="Lista de Compras", anchor="w")
    label.pack(fill="x", padx=5, pady=0)
