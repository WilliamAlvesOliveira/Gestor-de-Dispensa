from PIL import Image
import customtkinter as ctk
import logging
from .db import add_item_to_db

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

