from PIL import Image
import customtkinter as ctk
import threading
import time
import logging
from .db import add_item_to_db, edit_quantity_in_db, find_item_in_db, get_items_from_db, edit_item_in_db

# Configuração do logging
logging.basicConfig(level=logging.DEBUG)

def clear_frame(frame):
    """Remove todos os widgets do frame."""
    for widget in frame.winfo_children():
        widget.destroy()


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
            default_val = item[2]
            if variable_name not in variables:
                variables[variable_name] = ctk.StringVar(value=default_val)
            radio_frame = ctk.CTkFrame(parent, fg_color="white")
            radio_frame.pack(padx=2, pady=2, anchor="n")
            # Itera somente a partir do índice 3, para não duplicar o valor default
            for radio_text in item[3:]:
                ctk.CTkRadioButton(
                    radio_frame,
                    text=radio_text,
                    variable=variables[variable_name],
                    value=radio_text
                ).pack(side="left", padx=3, pady=3)
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


def validate_values(action, item_name, entries):
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

    if action == 'adicionar':
        add_result = add_item_to_db(values)
        
        if add_result["status"]:
            return {"status": True, "mensagem": f"O Produto '{nome}' foi adicionado com sucesso!"}
        return {"status": False, "mensagem": f"Erro ao adicionar o Produto '{nome}': {add_result['mensagem']}"}
    
    if action == 'editar':
        print(item_name)
        edit_item = item_name
        fields = ['nome', 'quantidade', 'target', 'essencial', 'periodo_de_compra']
        itens = get_items_from_db(fields)

        original_item = [item for item in itens if item['nome'] == edit_item]
       
        create_edit_query(item_name, original_item[0], values)

        return {"status": True, "mensagem": f"O Produto '{nome}' foi adicionado com sucesso!"}
           
    
def update_message(action,item_name, entries, message_label, form):
    """Atualiza a mensagem na interface e adiciona ao banco se os valores forem válidos."""
    resultado = validate_values(action, item_name, entries)
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

            
def create_edit_grid(frame, itens):
    container_frame = ctk.CTkFrame(frame, fg_color='white')
    container_frame.pack(fill="both", expand=True, padx=10, pady=10)

    grid_layout = ctk.CTkFrame(container_frame, fg_color='white')
    grid_layout.pack(fill="both", expand=True, padx=10, pady=10)

    for column in range(4):
        grid_layout.grid_columnconfigure(column, weight=1)
    grid_layout.grid_columnconfigure(2, weight=10)
    
    status_message = create_label(container_frame, '', 14)
    status_message.pack(fill='x', padx=5, pady=5)

    entries = create_grid_entries(container_frame, grid_layout, itens, status_message)

    update_all_button = ctk.CTkButton(container_frame, width=200, text='Atualizar todos os Itens', corner_radius=1000, fg_color='green')
    update_all_button.configure(command=lambda: validate_edit_values(
        [{'nome': data['nome'], 'quantidade': data['quantidade'].get()} for data in entries if data['quantidade'].get() != ''],
        update_all_button,
        update_all_button.cget("text"),
        status_message
    ))
    update_all_button.pack(padx=10, pady=10)

    return container_frame


def create_grid_entries(container, grid_layout, itens, status_message):
    entries = []
    for indice, item in enumerate(itens):
        create_button(grid_layout, None, 'Editar', lambda item=item: create_edit_item_form(container, item['nome']), 'blue', indice, 0)
        
        create_label(grid_layout, item["nome"][0].upper() + item["nome"][1:] if item["nome"] else "", 20).grid(padx=15, row=indice, column=1, sticky='w')
        
        entry_quantity = ctk.CTkEntry(grid_layout, width=50, placeholder_text=str(item['quantidade']))
        entry_quantity.grid(padx=15, row=indice, column=2, sticky='e')
        
        entries.append({'nome': item['nome'], 'quantidade': entry_quantity})
        
        update_button = create_button(grid_layout, None, 'Atualizar', None, 'green', indice, 3)
        update_button.configure(width=0, command=lambda item=item, entry=entry_quantity, btn=update_button: validate_edit_values([{'nome': item['nome'], 'quantidade': entry.get()}], btn, btn.cget('text'), status_message))
    
    return entries


def validate_edit_values(items, button, button_text, status_message):
    logging.info('Verificando valores editados')
    valid_items = []
    
    for item in items:
        if item['quantidade'] and item['quantidade'].isdigit() and int(item['quantidade']) >= 0:
            valid_items.append({'nome': item['nome'], 'quantidade': int(item['quantidade'])})
        else:
            error_message = f"Erro: Valor inválido para '{item['nome']}' ({item['quantidade']})"
            logging.error(error_message)
            if status_message:
                status_message.configure(text=error_message, text_color="red")
            animate_button_text(button, button_text, success=False)
            return
    
    if valid_items:
        edit_quantity_in_db(valid_items)
        logging.info("Todos os valores são válidos. Atualizando os itens.")
        if status_message:
            status_message.configure(text="Sucesso: Todos os itens foram atualizados.", text_color="green")
        animate_button_text(button, button_text, success=True)


def animate_button_text(button, original_text, success=True):
    def update_text(i=0):
        if i < 3:
            button.configure(text="." * (i + 1))
            button.after(300, update_text, i + 1)
        else:
            button.configure(text="✓" if success else "✗", fg_color="green" if success else "red")
            button.after(1000, lambda: button.configure(text=original_text, fg_color="green"))
    
    update_text()



def create_edit_item_form(frame, item_name):
    logging.info("Acessando tela de Editar Itens...")
    clear_frame(frame)
    
    fields = ['nome', 'quantidade', 'target', 'essencial', 'periodo_de_compra']
    find_item = find_item_in_db(item_name, fields)
    item_data = find_item["item"] if find_item["status"] else {}
    
    essencial_default = "Sim" if item_data.get("essencial", 0) == 1 else "Não"
    
    form = [
        ("label", "Nome do Produto *"),
        ("input", "Nome do Produto", item_data.get("nome", "")),
        ("label", "Quantidade *"),
        ("input", "Quantidade", str(item_data.get("quantidade", "0"))),
        ("label", "Quantidade de Referência *"),
        ("input", "Quantidade de Referência", str(item_data.get("target", ""))),
        ("label", "Essencial"),
        ("radio", "Essencial", essencial_default, "Sim", "Não"),
        ("label", "Período de Compra"),
        ("radio", "Periodo de Compra", item_data.get("periodo_de_compra", "Mensal"), "Mensal", "Quinzenal", "Semanal"),
    ]
    
    entries = create_form(frame, form)

    status_message = create_label(frame, '', 14)
    status_message.pack(fill='x', padx=5, pady=5)

    button_frame = ctk.CTkFrame(frame, fg_color="white")
    button_frame.pack(pady=20)

    editar_item = ctk.CTkButton(button_frame, text="Editar Item", corner_radius=1000, fg_color="green", font=("Arial",16), command=lambda: update_message('editar',item_name,entries, status_message, form))
    editar_item.pack(side="left", padx=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancelar", corner_radius=1000, fg_color="red", font=("Arial",16), command=lambda : restore_create_edit_grid(frame))
    cancel_button.pack(side="left", padx=10)


def restore_create_edit_grid(frame):
    clear_frame(frame)

    fields = ['nome', 'quantidade', 'periodo_de_compra']
    itens = get_items_from_db(fields)

    create_edit_grid(frame, itens)


def create_edit_query(item_name, original, edited):
    query_list = {}
    if original['nome'] != edited['nome']:
        query_list['nome'] = edited['nome']
    if original['quantidade'] != edited['quantidade']:
        query_list['quantidade'] = edited['quantidade']
    if original['target'] != edited['quantidade_referencia']:
        query_list['target'] = edited['quantidade_referencia']
    if original['essencial'] != edited['essencial']:
        query_list['essencial'] = edited['essencial']
    if original['periodo_de_compra'] != edited['periodo']:
        query_list['periodo_de_compra'] = edited['periodo']

    edit_item_in_db(item_name, query_list)

