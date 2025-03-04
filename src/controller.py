from .db import connection_test, get_items_from_db
from .utils import create_label,  create_scrollable_frame, create_form, update_message
import customtkinter as ctk
import logging

import logging

def show_results(label_result):
    """Atualiza o label de resultado com o status da conexão."""
    try:
        logging.info("Testando conexão com o banco de dados...")
        result = connection_test()
        message = "✅ Conexão bem-sucedida com o banco de dados 'dispensa'." if result else "❌ Erro ao conectar ao banco de dados."
        label_result.configure(text=message, text_color="green" if result else "red")
    except Exception as e:
        logging.error(f"Erro ao conectar: {e}")
        label_result.configure(text="❌ Exceção ao tentar conectar ao banco de dados.", text_color="red")


def clear_frame(frame):
    """Remove todos os widgets do frame."""
    for widget in frame.winfo_children():
        widget.destroy()


def boas_vindas(frame):
    """Cria a tela de boas-vindas."""
    welcome_frame = ctk.CTkFrame(frame, fg_color="white")
    labels = [
        ("Seja bem-vindo ao app", 16),
        ("Gerenciador de Dispensa", 26, "bold"),
        ("Selecione a opção que deseja utilizar", 16)
    ]
    for text, size, *style in labels:
        create_label(welcome_frame, text, size, *style).pack(pady=10)
    welcome_frame.pack(expand=True)
    return welcome_frame


def add_item_frame(frame):
    """Cria o frame para adicionar itens com barra de rolagem."""
    logging.info("Acessando tela de adição de itens...")
    clear_frame(frame)
    scrollable_frame = create_scrollable_frame(frame)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    # Título do frame
    create_label(scrollable_frame, "Adicionar Item", 22, "bold").pack(fill="x", padx=5, pady=5)

    # Formulário de adição de itens
    form = [
        ("label", "Nome do Produto *"),
        ("input", "Nome do Produto", "Digite o nome do Produto"),
        ("label", "Quantidade *"),
        ("input", "Quantidade", "0"),
        ("label", "Quantidade de Referência *"),
        ("input", "Quantidade de Referência", "Digite a quantidade a ser mantida"),
        ("label", "Essencial"),
        ("radio", "Essencial", "Sim", "Não"),
        ("label", "Período de Compra"),
        ("radio", "Periodo de Compra", "Mensal", "Quinzenal", "Semanal"),
    ]
    entries = create_form(scrollable_frame, form)

    # Mensagem de feedback
    message_label = ctk.CTkLabel(scrollable_frame, text="", font=("Arial", 18))
    message_label.pack(fill="x", padx=5, pady=5)

    # Botão de adicionar item
    ctk.CTkButton(
        scrollable_frame,
        text="Adicionar Item",
        command=lambda: update_message(entries, message_label, form),
        fg_color="green"
    ).pack(padx=6, pady=5)

    return scrollable_frame


def remove_item_frame(frame):
    """Cria o frame para remover itens."""
    logging.info("Acessando tela de remoção de itens...")
    clear_frame(frame)
    scrollable_frame = create_scrollable_frame(frame)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    # Título do frame
    create_label(scrollable_frame, "Remover Item", 22, "bold").pack(fill="x", padx=5, pady=5)

    # Formulário de remoção de itens
    create_form(scrollable_frame, [
        ("label", "Nome do produto que você deseja excluir:"),
        ("input", "Nome do produto", "Nome do produto")
    ])

    return scrollable_frame

def edit_item_frame(frame):
    logging.info("Botão: Editar Item foi clicado!")

    for widget in frame.winfo_children():
        widget.destroy()

    edit_frame = ctk.CTkFrame(frame, fg_color="white")
    edit_frame.pack(fill="both", expand=True, padx=10, pady=10)

    label = ctk.CTkLabel(edit_frame, text="Editar Item", anchor="w")
    label.pack(fill="x", padx=5, pady=0)

    return edit_frame


def show_list_frame(frame):
    """Exibe os itens cadastrados."""
    logging.info("Acessando tela de listagem de itens...")
    clear_frame(frame)
    scrollable_frame = create_scrollable_frame(frame)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    # Título do frame
    create_label(scrollable_frame, "Itens da Dispensa", 24, "underline", "bold").pack(fill="x", padx=20, pady=20)

    # Busca os itens no banco de dados
    items = get_items_from_db()

    # Verifica se há itens
    if isinstance(items, str) or not items:
        error_message = items if isinstance(items, str) else "Não há itens na sua dispensa!"
        create_label(scrollable_frame, error_message, 24, "bold").pack(pady=20)
        return scrollable_frame

    # Exibe os itens
    for item in items:
        item_frame = ctk.CTkFrame(scrollable_frame, width=400, height=50)
        item_frame.pack(padx=10, pady=5, anchor="center")
        item_frame.pack_propagate(False)

        # Nome do produto com a primeira letra maiúscula sem alterar o restante
        product_name = item["nome"][0].upper() + item["nome"][1:] if item["nome"] else ""
        create_label(item_frame, product_name, 20).pack(side="left", padx=10, pady=5)

        # Quantidade do produto
        quantity_label = create_label(item_frame, str(item["quantidade"]), 20)
        quantity_label.configure(text_color="red" if item["quantidade"] < item["target"] else "green")
        quantity_label.pack(side="right", padx=10, pady=5)

    return scrollable_frame




def shop_list_frame(frame):

    logging.info("Botão: Lista de Compras foi clicado!")

    for widget in frame.winfo_children():
        widget.destroy()

    shop_list = ctk.CTkFrame(frame, fg_color="white")
    shop_list.pack(fill="both", expand=True, padx=10, pady=10)

    label = ctk.CTkLabel(shop_list, text="Lista de Compras", anchor="w")
    label.pack(fill="x", padx=5, pady=0)

