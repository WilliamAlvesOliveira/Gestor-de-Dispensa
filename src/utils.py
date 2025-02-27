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

