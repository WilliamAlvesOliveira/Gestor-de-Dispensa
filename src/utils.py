from PIL import Image
import customtkinter as ctk
import threading
import time
import logging
from .db import add_item_to_db, edit_quantity_in_db


# Configuração do logging
logging.basicConfig(level=logging.DEBUG)

def load_img(image_path, size=(50, 50)):
    """Carrega uma imagem e redimensiona se necessário."""
    try:
        img = Image.open(image_path)
        img = img.resize(size)
        return ctk.CTkImage(light_image=img, dark_image=img)
    except Exception as e:
        logging.error(f"Erro ao carregar imagem '{image_path}': {e}")
        return None


def create_label(parent, text, font_size, *style):
    """Cria e retorna um label formatado."""
    return ctk.CTkLabel(parent, text=text, font=("Helvetica", font_size, *style))


def create_button(parent, image_path, text, command=None, fg_color="gray", row=0, column=0):
    """Cria um botão com imagem e texto."""
    img = load_img(image_path) if image_path else None 
    button = ctk.CTkButton(
        parent,
        image=img if img else None,
        text=text,
        command=command if command else lambda: logging.info(f"Botão {text} pressionado"),
        fg_color=fg_color,
        compound="top"
    )
    
    if img:
        button.image = img  # Evita que a imagem seja coletada pelo garbage collector

    button.grid(row=row, column=column, sticky="nsew")

    return button


def create_scrollable_frame(parent):
    """Cria um frame rolável dentro do canvas."""
    canvas = ctk.CTkCanvas(parent, bg="white")
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ctk.CTkScrollbar(parent, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")
    
    def resize_scrollable_frame(event):
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())
    canvas.bind("<Configure>", resize_scrollable_frame)
    
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    scrollable_frame.bind("<Configure>", configure_scroll_region)
    
    return scrollable_frame


def create_form(parent, form):
    """Cria os elementos do formulário dinamicamente."""
    entries = {}
    variables = {}
    
    for item in form:
        element_type, text = item[:2]
        if element_type == "label":
            ctk.CTkLabel(parent, text=text, anchor="n").pack(fill="x", padx=2, pady=2)
        elif element_type == "input":
            entry = ctk.CTkEntry(parent, width=400)
            entry.pack(padx=2, pady=2, anchor="n")
            if len(item) > 2:
                add_placeholder(entry, item[2])
            entries[text] = entry
        elif element_type == "radio":
            variable_name = text
            if variable_name not in variables:
                variables[variable_name] = ctk.StringVar(value=item[2])
            radio_frame = ctk.CTkFrame(parent, fg_color="white")
            radio_frame.pack(padx=2, pady=2, anchor="n")
            for radio_text in item[2:]:
                ctk.CTkRadioButton(radio_frame, text=radio_text, variable=variables[variable_name], value=radio_text).pack(side="left", padx=3, pady=3)
            entries[text] = variables[variable_name]
    return entries


def add_placeholder(entry, placeholder):
    """Adiciona um placeholder ao campo de entrada."""
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda event: clear_placeholder(event, entry, placeholder))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(event, entry, placeholder))


def clear_placeholder(event, entry, placeholder):
    """Limpa o placeholder quando o campo é focado."""
    if entry.get() == placeholder:
        entry.delete(0, "end")


def restore_placeholder(event, entry, placeholder):
    """Restaura o placeholder quando o campo perde o foco."""
    if entry.get() == "":
        entry.insert(0, placeholder)


def validate_values(entries):
    """Valida os valores dos campos de entrada."""
    nome = entries["Nome do Produto"].get().strip()
    quantidade = entries["Quantidade"].get().strip()
    quantidade_referencia = entries["Quantidade de Referência"].get().strip()
    quantidade_referencia = '1' if quantidade_referencia in ['0', "Digite a quantidade a ser mantida"] else quantidade_referencia
    essencial = entries["Essencial"].get() == "Sim"
    periodo = entries["Periodo de Compra"].get()
    
    if not nome or nome == "Digite o nome do Produto":
        return {"status": False, "mensagem": "Preencha o Nome do Produto!"}
    if not quantidade.isdigit() or int(quantidade) < 0:
        return {"status": False, "mensagem": "Quantidade deve ser maior ou igual a 0!"}
    if not quantidade_referencia.isdigit():
        return {"status": False, "mensagem": "Preencha o campo Quantidade de Referência com um valor acima de 0!"}
    
    values = {"nome": nome, "quantidade": int(quantidade), "quantidade_referencia": int(quantidade_referencia), "essencial": essencial, "periodo": periodo}
    add_result = add_item_to_db(values)
    
    if add_result["status"]:
        return {"status": True, "mensagem": f"O Produto '{nome}' foi adicionado com sucesso!"}
    return {"status": False, "mensagem": f"Erro ao adicionar o Produto '{nome}': {add_result['mensagem']}"}

    
def update_message(entries, message_label, form):
    """Atualiza a mensagem na interface e adiciona ao banco se os valores forem válidos."""
    resultado = validate_values(entries)
    message_label.configure(text=resultado["mensagem"], text_color="green" if resultado['status'] else "red")
    if resultado['status']:
        clear_form(entries, form)


def clear_form(entries, form):
    """Limpa os campos do formulário mantendo os placeholders."""
    for item in form:
        element_type, text = item[:2]
        if element_type == "input" and text in entries:
            placeholder = item[2] if len(item) > 2 else ""
            entry = entries[text]
            entry.delete(0, 'end')
            if placeholder:
                entry.insert(0, placeholder)
        elif element_type == "radio" and text in entries:
            entries[text].set(item[2])

            
def edit_grid(frame, itens):
    grid_layout = ctk.CTkFrame(frame, fg_color='white')
    grid_layout.pack(fill="both", expand=True, padx=10, pady=10)

    # Configura 4 colunas com peso igual.
    for column in range(0, 4):
        grid_layout.grid_columnconfigure(column, weight=1)

    entries = []

    # Cria um frame para a mensagem de status.
    confirm_all_frame = ctk.CTkFrame(frame, fg_color='white')
    confirm_all_frame.pack(fill='x', padx=10, pady=10)

    # Cria o widget status_message que exibirá o feedback de cada operação.
    status_message = create_label(confirm_all_frame, '', 14)
    status_message.pack(fill='x', padx=5, pady=0)

    # Função para criar o comando de atualização para cada item individual
    def create_update_command(nome, entry, btn):
        return lambda: validate_edit_values(
            [{'nome': nome, 'quantidade': entry.get()}],
            btn,
            btn.cget('text'),
            status_message
        )

    # Cria as linhas da grid para cada item
    for indice, item in enumerate(itens):
        edit = create_button(grid_layout, None, 'Editar', None, 'blue', indice, 0)
        edit.configure(width=0)
        
        # Cria um rótulo com o nome do produto
        create_label(grid_layout, item['nome'], 20).grid(padx= 15, row=indice, column=1, sticky='w')
        
        # Cria a entrada para a quantidade, com o placeholder sendo a quantidade atual
        entry_quantity = ctk.CTkEntry(grid_layout, width=50, placeholder_text=str(item['quantidade']))
        entry_quantity.grid(padx=15, row=indice, column=2, sticky='e')
        entries.append({'nome': item['nome'], 'quantidade': entry_quantity})
        
        # Botão para atualizar o item individual
        atualizar = create_button(grid_layout, None, 'Atualizar', None, 'green', indice, 3)
        atualizar.configure(width=0, command=create_update_command(item['nome'], entry_quantity, atualizar))

    # Botão "Atualizar todos os Itens"
    atualizar_todos = ctk.CTkButton(
        confirm_all_frame,
        width=200,
        text='Atualizar todos os Itens',
        corner_radius=1000,
        fg_color='green'
    )
    atualizar_todos.configure(
        command=lambda: validate_edit_values(
            [{'nome': data['nome'], 'quantidade': data['quantidade'].get()} for data in entries],
            atualizar_todos,
            atualizar_todos.cget("text"),
            status_message
        )
    )
    atualizar_todos.pack(padx=10, pady=10)

    return grid_layout


def validate_edit_values(items, button, button_text, status_message):
    logging.info('Verificando valores editados')
    query_itens = []

    for item in items:
        if item['quantidade'] != '':
            if not item['quantidade'].isdigit() or int(item['quantidade']) < 0:
                error_message = (
                    f"Valor inválido para o produto '{item.get('nome')}'. "
                    f"Valor recebido: '{item['quantidade']}'"
                )
                logging.error(error_message)
                animate_button_text(button, button_text, success=False)
                status_message.configure(text=f"Erro: {error_message}", text_color="red")
                return
            else:
                query_itens.append({
                    'nome': item.get('nome'),
                    'quantidade': int(item['quantidade'])
                })

    if len(query_itens) > 0:
        edit_quantity_in_db(query_itens)

    logging.info("Todos os valores são válidos. Atualizando os itens.")
    animate_button_text(button, button_text, success=True)
    status_message.configure(text="Sucesso: Todos os itens foram atualizados.", text_color="green")


def animate_button_text(button, original_text, success=True):
    """Anima o botão sem travar a interface."""
    def update_text():
        for i in range(3):
            button.configure(text="." * (i + 1))
            button.update()
            time.sleep(0.8)
        
        button.configure(text="✓" if success else "✗", fg_color="green" if success else "red")
        button.update()
        time.sleep(1)
        
        button.configure(text=original_text, fg_color="green")
        button.update()

    threading.Thread(target=update_text, daemon=True).start()
