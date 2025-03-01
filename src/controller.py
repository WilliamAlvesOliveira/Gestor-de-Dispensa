from .db import connection_test, get_items_from_db
from .utils import create_scrollable_frame, create_form, create_button
import customtkinter as ctk
import logging

import logging

def show_results(label_result):
    """Atualiza o label de resultado com o status da conexão."""
    try:
        logging.info("Botão clicado! Tentando conexão...")
        result = connection_test()
        if result:
            label_result.configure(text="✅ Conexão bem-sucedida com o banco de dados 'dispensa'.", text_color="green")
        else:
            label_result.configure(text="❌ Erro ao conectar ao banco de dados.", text_color="red")
    except Exception as e:
        label_result.configure(text="❌ Exceção ao tentar conectar ao banco de dados.", text_color="red")


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
    """Cria o frame para adicionar itens com barra de rolagem"""

    logging.info("Botão Adicionar Item clicado!")

    # Limpa o frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Cria o frame rolável usando a função reutilizável
    scrollable_frame = create_scrollable_frame(frame)

    # Configura o grid do frame rolável para expandir e preencher o espaço disponível
    scrollable_frame.grid_columnconfigure(0, weight=1)

    label = ctk.CTkLabel(scrollable_frame, text="Adicionar Item", font=("Times", 22,"bold"), anchor="n")
    label.pack(fill="x", padx=5, pady=5)

    # Lista de elementos do formulário
    form = [
        #tipo do elemento,nome do label, texto para as labels
        #tipo do input, nome do label, placeholder 
        #tipo radio, nome do label, textos de cada botão
        ("label", "Nome do Produto *"),
        ("input", "Nome do Produto","Digite o nome do Produto"),
        ("label", "Quantidade"),
        ("input", "Quantidade","0"),
        ("label", "Quantidade de Referência"),
        ("input", "Quantidade de Referência","Digite a quantidade a ser mantida"),
        ("label", "Essencial?"),
        ("radio", "essencial", "Sim", "Não"),
        ("label", "Período de Compra"),
        ("radio", "periodo de Compra", "Mensal", "Quinzenal", "Semanal"),
    ]

    # Cria os elementos do formulário dinamicamente
    create_form(scrollable_frame, form)

    button = ctk.CTkButton( scrollable_frame,  text="Adicionar Item", command= lambda : logging.info("clicado"), fg_color="green")
    button.pack( padx=6, pady=5, anchor="n")

    return scrollable_frame


def remove_item_frame(frame):

    logging.info("Botão: Remover Item foi clicado!")

    for widget in frame.winfo_children():
        widget.destroy() # remove todos os widgets

    scrollable_frame = create_scrollable_frame(frame)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    label = ctk.CTkLabel(scrollable_frame, text="Remover Item", font=("Times", 22,"bold"), anchor="n")
    label.pack(fill="x", padx=5, pady=5)

    # Lista de elementos do formulário
    form = [
        ("label", "Nome do produto que você deseja excluir:"),
        ("input", "Nome do produto que você deseja excluir:","Nome do produto")
    ]

    # Cria os elementos do formulário dinamicamente
    create_form(scrollable_frame, form)

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
    logging.info("Botão: Itens da Dispensa foi clicado!, tentando conexão com o banco de dados...")

    # Limpa o frame antes de exibir os novos itens
    for widget in frame.winfo_children():
        widget.destroy()

    scrollable_frame = create_scrollable_frame(frame)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    label = ctk.CTkLabel(scrollable_frame, text="Itens da Dispensa", font=("Times", 24, "underline", "bold"), anchor="n")
    label.pack(fill="x", padx=20, pady=20)

    items = get_items_from_db()

    if isinstance(items, str):  # Se houver uma mensagem de erro, mostra a mensagem de erro
        error_label = ctk.CTkLabel(
            scrollable_frame,
            text=items,
            font=("Arial", 24, "bold"),
            text_color="red",  # Define a cor do texto como vermelho
            anchor="center",
            wraplength=400  # Limita a largura do texto para melhor exibição
        )
        error_label.pack(pady=20)
        return scrollable_frame

    if not items:  # Se a lista estiver vazia
        error_label = ctk.CTkLabel(
            scrollable_frame,
            text="Não há items na sua dispensa!",
            font=("Arial", 24, "bold"),
            text_color="red",
            anchor="center",
            wraplength=400 
        )
        error_label.pack(pady=20)
        return scrollable_frame

    # Se houver itens, exibe a lista normalmente
    for item in items:
        item_name = item["nome"]
        item_quantity = item["quantidade"]
        item_target = item["target"]

        # Define a cor da quantidade
        quantity_color = "red" if item_quantity < item_target else "green"

        # Criação do frame para cada item
        item_frame = ctk.CTkFrame(scrollable_frame, width=400, height=50)
        item_frame.pack(padx=10, pady=5, anchor="center")
        item_frame.pack_propagate(False) #impede que o frame se ajuste ao conteúdo mantendo o tamanho estabelecido: 400px

        # Nome do item
        item_label = ctk.CTkLabel(item_frame, text=item_name, font=("arial",20), anchor="w")
        item_label.pack(side="left", padx=10, pady=5)

        # Quantidade do item
        quantity_label = ctk.CTkLabel(item_frame, text=str(item_quantity), font=("arial",20), anchor="e")
        quantity_label.pack(side="right", padx=10, pady=5)
        quantity_label.configure(text_color=quantity_color)

    return scrollable_frame


def shop_list_frame(frame):

    logging.info("Botão: Lista de Compras foi clicado!")

    for widget in frame.winfo_children():
        widget.destroy()

    shop_list = ctk.CTkFrame(frame, fg_color="white")
    shop_list.pack(fill="both", expand=True, padx=10, pady=10)

    label = ctk.CTkLabel(shop_list, text="Lista de Compras", anchor="w")
    label.pack(fill="x", padx=5, pady=0)

