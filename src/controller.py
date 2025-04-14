from .db import connection_test, get_items_from_db, find_item_in_db, delete_item_from_db
from .utils import clear_frame, create_label,  create_scrollable_frame, create_form, update_message, create_button, create_edit_grid
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

    essencial_default = "Sim"
    # Formulário de adição de itens
    form = [
        ("label", "Nome do Produto *"),
        ("input", "Nome do Produto", "Digite o nome do Produto"),
        ("label", "Quantidade *"),
        ("input", "Quantidade", "0"),
        ("label", "Quantidade de Referência *"),
        ("input", "Quantidade de Referência", "Digite a quantidade a ser mantida"),
        ("label", "Essencial"),
        ("radio", "Essencial", essencial_default, "Sim", "Não"),
        ("label", "Período de Compra"),
        ("radio", "Periodo de Compra",'Mensal', "Mensal", "Quinzenal", "Semanal"),
    ]
    
    entries = create_form(scrollable_frame, form)

    # Mensagem de feedback
    message_label = ctk.CTkLabel(scrollable_frame, text="", font=("Arial", 18))
    message_label.pack(fill="x", padx=5, pady=5)

    # Botão de adicionar item
    ctk.CTkButton(
        scrollable_frame,
        text="Adicionar Item",
        command=lambda: update_message('adicionar',None, entries, message_label, form),
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
    
    #Mensagem de erro na busca
    search_error = create_label(scrollable_frame, "",12)
    search_error.pack(fill="x",padx=5, pady=2)
    search_error.configure(text_color="red")
   
    # Campo de busca
    search_frame = ctk.CTkFrame(scrollable_frame, fg_color="white")
    search_frame.pack(anchor="center", padx=10, pady=5)

    create_label(search_frame, "Encontrar produto:", 16, "bold").pack(side="left", padx=5)

    search_entry = ctk.CTkEntry(search_frame, placeholder_text="Nome do produto", width=200)
    search_entry.pack(side="left", padx=5)
    
    search_button = ctk.CTkButton(search_frame, text="buscar", corner_radius=1000, fg_color="green", font=("Arial",16,"bold"),command=lambda: search_product(frame, search_entry, search_error))
    search_button.pack(side="left", padx=5)

    fields = ["nome"]
    items = get_items_from_db(fields)

    if isinstance(items, str) or not items:
        error_message = items if isinstance(items, str) else "Não há itens na sua dispensa!"
        error_label = create_label(scrollable_frame, error_message, 24, "bold")
        error_label.configure(text_color="red")
        error_label.pack(pady=20)
        return scrollable_frame
    
    for item in items:
        item_frame = ctk.CTkFrame(scrollable_frame,width=400, height=50)
        item_frame.pack(anchor="center", padx=10, pady=5)
        item_frame.pack_propagate(False)

        product_name = item["nome"][0].upper() + item["nome"][1:] if item["nome"] else ""
        remove_button = create_button(item_frame, None, product_name, command= lambda  nome=item["nome"]: confirm_remove_item(frame, nome), fg_color="red", row=0, column=0)
        remove_button.configure(font=("Arial", 18, 'underline'))
        
    return scrollable_frame


def search_product(frame, entry, label):
    """Busca produto para remoção e exibe resultado"""
    produto_name = entry.get().strip()
    if not produto_name:
        label.configure(text="Por favor, digite um nome válido.", text_color="red")
        return

    logging.info(f"Buscando por: {produto_name}")
    search_result = find_item_in_db(produto_name, ["nome"])
    
    if search_result["status"]:
        logging.info(f'Produto encontrado: {search_result["item"]["nome"]}')
        confirm_remove_item(frame, search_result["item"]["nome"])
    else:
        label.configure(text="Produto não encontrado", text_color="red")



def confirm_remove_item(frame, item_name):
    """Confirma a remoção do item."""
    logging.info(f"O produto {item_name} foi selecionado.")
    clear_frame(frame)

    # Buscar informações do item
    fields = ["nome", "quantidade", "target"]
    results = find_item_in_db(item_name, fields)
    if not results["status"]:
        error_message = results["mensagem"]
        error_label = create_label(frame, error_message, 24, "bold")
        error_label.pack(pady=20)
        error_label.configure(text_color="red")  # Ajustar para usar text_color
        return frame

    item = results["item"]

    # Mensagem de confirmação
    confirm_label = create_label(frame, f"Tem certeza que deseja remover o item:", 16, "bold")
    confirm_label.pack(pady=20)
    confirm_label.configure(text_color="red")  # Ajustar para usar text_color

    # Informações do item
    item_frame = ctk.CTkFrame(frame, width=400, height=50)
    item_frame.pack(padx=10, pady=5, anchor="center")
    item_frame.pack_propagate(False)

    product_name = item["nome"][0].upper() + item["nome"][1:] if item["nome"] else ""
    create_label(item_frame, product_name, 20).pack(side="left", padx=10, pady=5)

    quantity_label = create_label(item_frame, str(item["quantidade"]), 20)
    quantity_label.configure(text_color="red" if item["quantidade"] < item["target"] else "green")
    quantity_label.pack(side="right", padx=10, pady=5)

    # Botões de confirmação e cancelamento
    button_frame = ctk.CTkFrame(frame, fg_color="white")
    button_frame.pack(pady=20)

    yes_button = ctk.CTkButton(button_frame, text="Confirmar", corner_radius=1000, fg_color="red", font=("Arial",20,"bold"), command= lambda : handle_delete_item(item["nome"],frame))
    yes_button.pack(side="left", padx=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancelar", corner_radius=1000, fg_color="blue", font=("Arial",20,"bold"), command=lambda :remove_item_frame(frame))
    cancel_button.pack(side="left", padx=10)


def handle_delete_item(item_name, frame):
    """Lida com a remoção do item e exibe a mensagem de sucesso ou erro."""
    clear_frame(frame)

    result = delete_item_from_db(item_name)

    # Criar um novo frame para a mensagem
    message_frame = ctk.CTkFrame(frame, fg_color="white")
    message_frame.pack(pady=20)

    # Adicionar a mensagem no frame de mensagem
    message_label = create_label(message_frame, result["mensagem"], 24, "bold")
    message_label.pack(pady=20)
    message_label.configure(text_color="green" if result["status"] else "red")

    button_frame = ctk.CTkFrame(frame, fg_color="white")
    button_frame.pack(pady=20, padx=10, anchor="center")

    back_button = ctk.CTkButton(button_frame, text="Voltar", corner_radius=1000, fg_color="blue", font=("Arial", 20, "bold"), command=lambda: remove_item_frame(frame))
    back_button.pack(pady=10)


def edit_item_frame(frame):
    logging.info("Acessando a tela de edição de itens")
    clear_frame(frame)
    
    scrollable_frame = create_scrollable_frame(frame)
    scrollable_frame.grid_columnconfigure(0, weight=1)
    
    create_label(scrollable_frame, 'Editar Itens', 22, 'bold').pack(fill='x', padx=5, pady=5)
    
    fields = ['nome', 'quantidade', 'periodo_de_compra']
    itens = get_items_from_db(fields)
    
    edit_frame = create_edit_grid(scrollable_frame, itens)
    edit_frame.pack(fill='x', padx=10, pady=10)
    
    return scrollable_frame


def show_list_frame(frame):
    """Exibe os itens cadastrados."""
    logging.info("Acessando tela de listagem de itens...")
    clear_frame(frame)
    scrollable_frame = create_scrollable_frame(frame)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    # Título do frame
    create_label(scrollable_frame, "Itens da Dispensa", 24, "underline", "bold").pack(fill="x", padx=20, pady=20)

    # Busca os itens no banco de dados
    fields = ["nome","quantidade","target"]
    items = get_items_from_db(fields)

    # Verifica se há itens
    if isinstance(items, str) or not items:
        error_message = items if isinstance(items, str) else "Não há itens na sua dispensa!"
        error_label = create_label(scrollable_frame, error_message, 24, "bold")
        error_label.configure(text_color="red")
        error_label.pack(pady=20)
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
    """função para criar o frame de lista de compras"""
    logging.info("Botão: Lista de Compras foi clicado!")

    clear_frame(frame)
    scrollable_frame = create_scrollable_frame(frame)
    scrollable_frame.grid_columnconfigure(0, weight=1)

    create_label(scrollable_frame, "Lista de Compras", 24, 'underline').pack(fill='x', padx=10, pady=10)

    fields = ["nome", "quantidade","target", 'essencial']
    itens = get_items_from_db(fields)

    itens_essenciais  =[]
    outros  = []
    for item in itens:
        if item['quantidade']<item['target']:
            if bool(item['essencial']):
                produto = {'nome' : item['nome'], 'quantidade': item['target'] - item['quantidade']}
                itens_essenciais.append(produto)
            else:
               produto = {'nome' : item['nome'], 'quantidade': item['target'] - item['quantidade']}
               outros.append(produto)
               
    logging.info('Gerando lista de compras')

    for produtos in itens_essenciais:
        essential_items_frame = ctk.CTkFrame(scrollable_frame, width=400, height=50)
        essential_items_frame.pack(padx=10, pady=5, anchor="center")
        essential_items_frame.pack_propagate(False)
    
        product_label = create_label(essential_items_frame, produtos["nome"][0].upper() + produtos["nome"][1:] if produtos["nome"] else "", 24, "bold")
        product_label.pack(side="left", padx=3, pady=5, anchor='w')

        quantity_label = create_label(essential_items_frame, str(produtos["quantidade"]), 24, 'bold')
        quantity_label.pack(side='right', padx=5, pady=5)

    create_label(scrollable_frame, "Itens Complementares", 16, 'underline').pack(fill='x', padx=10, pady=10)

    for produtos in outros:
        itens_complementares_frame = ctk.CTkFrame(scrollable_frame, width=200, height=30)
        itens_complementares_frame.pack(padx=10, pady=5, anchor='center')
        itens_complementares_frame.pack_propagate(False)

        product_label= create_label(itens_complementares_frame, produtos["nome"][0].upper() + produtos["nome"][1:] if produtos["nome"] else "", 16, 'bold')
        product_label.pack(side='left', padx=5, pady=5, anchor='w')

        quantity_label = create_label( itens_complementares_frame, str(produtos['quantidade']), 16, 'bold')
        quantity_label.pack(side='right', padx=5, pady=5)

