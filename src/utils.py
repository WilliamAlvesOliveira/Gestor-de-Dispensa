from PIL import Image
import customtkinter as ctk
import logging

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


def create_button(parent, image_path, text, command=None, fg_color="gray", row=0, column=0):
    """Cria um botão com imagem e texto."""
    img = load_img(image_path)
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


def create_scrollable_frame(parent):
    """Cria um frame rolável dentro do canvas"""
    # Cria um canvas que conterá o frame rolável
    canvas = ctk.CTkCanvas(parent, bg="white")
    canvas.pack(side="left", fill="both", expand=True)

    # Adiciona a barra de rolagem ao canvas
    scrollbar = ctk.CTkScrollbar(parent, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configura o canvas para usar a barra de rolagem
    canvas.configure(yscrollcommand=scrollbar.set)

    # Cria um frame dentro do canvas
    scrollable_frame = ctk.CTkFrame(canvas, fg_color="white")
    
    # Adiciona o frame ao canvas
    canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

    # Faz com que o frame se expanda para preencher a largura do canvas
    def resize_scrollable_frame(event):
        canvas.itemconfig(canvas_window, width=canvas.winfo_width())

    canvas.bind("<Configure>", resize_scrollable_frame)

    # Função para ajustar a barra de rolagem conforme o conteúdo é adicionado
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_scroll_region)

    return scrollable_frame

def create_form(parent, form):
    """Cria os elementos do formulário dinamicamente"""
    variables = {}

    def add_placeholder(entry, placeholder):
        """Adiciona um placeholder ao campo de entrada"""
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: clear_placeholder(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event: restore_placeholder(event, entry, placeholder))

    def clear_placeholder(event, entry, placeholder):
        """Limpa o placeholder quando o campo é focado"""
        if entry.get() == placeholder:
            entry.delete(0, "end")

    def restore_placeholder(event, entry, placeholder):
        """Restaura o placeholder quando o campo perde o foco"""
        if entry.get() == "":
            entry.insert(0, placeholder)

    for item in form:
        element_type = item[0]  
        text = item[1]  

        if element_type == "label":
            label = ctk.CTkLabel(parent, text=text, anchor="n")
            label.pack(fill="x", padx=2, pady=2)
        elif element_type == "input":
            placeholder = item[2] if len(item) > 2 else ""
            entry = ctk.CTkEntry(parent, width=400)
            entry.pack(padx=2, pady=2, anchor="n")
            if placeholder:
                add_placeholder(entry, placeholder)
        elif element_type == "radio":
            variable_name = text  
            if variable_name not in variables:
                variables[variable_name] = ctk.StringVar(value=item[2])

            radio_frame = ctk.CTkFrame(parent, fg_color="white")
            radio_frame.pack(padx=2, pady=2, anchor="n")

            for i in range(2, len(item)):
                radio_text = item[i]
                radio_button = ctk.CTkRadioButton(radio_frame, text=radio_text, variable=variables[variable_name], value=radio_text)
                radio_button.pack(side="left", padx=3, pady=3)  # lado a lado
