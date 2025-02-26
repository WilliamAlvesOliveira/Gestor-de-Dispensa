from PIL import ImageTk, Image #importação do pillow
import customtkinter as ctk
import logging

# Configura o logging
logging.basicConfig(level=logging.DEBUG)

#função para carregar a imagem parametros: caminho, tamanho
def load_img(image_path, size=(50,50)):
    try:
        img = Image.open(image_path)
        
        img = img.resize(size) #caso necessite redimendionar a imagem
        return ctk.CTkImage(light_image=img, dark_image=img)
    except Exception as e:
        logging.error(f"Erro ao carregar imagem '{image_path}': {e}")
        return None  # Retorna None se houver erro

def create_button(parent, image_path, text, command, fg_color, row, column):
    """
    Função para criar e adicionar um botão a um container pai.
    :param parent: Container pai onde o botão será adicionado.
    :param image_path: Caminho para a imagem do botão.
    :param text: Texto do botão.
    :param command: Função a ser chamada ao clicar no botão.
    :param fg_color: Cor de fundo do botão.
    :param row: Linha onde o botão será posicionado.
    :param column: Coluna onde o botão será posicionado.
    """

    img = load_img(image_path)
    button = ctk.CTkButton(parent, image=img, text=text, command=command, fg_color=fg_color, compound="top")

    if img:
        button.configure(image=img)
        button.image = img  # Mantém uma referência para evitar problemas de exibição
        
    button.grid(row=row, column=column, sticky="nsew")