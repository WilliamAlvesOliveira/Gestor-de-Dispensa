import customtkinter as ctk
import logging
from .controller import (
    show_results, boas_vindas, add_item_frame, 
    remove_item_frame, edit_item_frame, 
    show_list_frame, shop_list_frame
)
from .utils import create_button

from .db import create_database_if_not_exists

# Configuração do logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DispensaApp(ctk.CTk):
    def __init__(self):
        """Inicializa a janela principal do aplicativo"""
        super().__init__()
        create_database_if_not_exists()
        self.title("Gerenciador de Dispensa")
        self.geometry('800x400')
        self.main_frame = None  # Inicializa como None para evitar erros
        self.label_result = None
        self.create_widgets()

    def create_widgets(self):
        """Cria e organiza os elementos visuais da interface"""
        screen = self._create_main_screen()
        self._create_option_bar(screen).grid(row=0, column=0, sticky="nsew")
        self.main_frame = self._create_main_frame(screen)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        boas_vindas(self.main_frame)
        self._create_test_area(screen).grid(row=2, column=0, sticky="nsew")

    def _create_main_screen(self):
        """Cria o frame principal"""
        screen = ctk.CTkFrame(self)
        screen.pack(fill="both", expand=True, padx=10, pady=0)
        screen.grid_rowconfigure(0, weight=5)
        screen.grid_rowconfigure(1, weight=93)
        screen.grid_rowconfigure(2, weight=2)
        screen.grid_columnconfigure(0, weight=1)
        return screen

    def _create_option_bar(self, parent):
        """Cria a barra superior com botões de navegação"""
        option_bar = ctk.CTkFrame(parent)
        for i in range(5):
            option_bar.grid_columnconfigure(i, weight=1)
        
        buttons = [
            ("Adicionar Item", "assets/imagens/add.png", lambda: add_item_frame(self.main_frame), "green"),
            ("Remover Item", "assets/imagens/remove.png", lambda: remove_item_frame(self.main_frame), "red"),
            ("Editar Item", "assets/imagens/edit.png", lambda: edit_item_frame(self.main_frame), "blue"),
            ("Mostrar Itens", "assets/imagens/itensList.png", lambda: show_list_frame(self.main_frame), "gray"),
            ("Lista de Compras", "assets/imagens/shopList.png", lambda: shop_list_frame(self.main_frame), "gray"),
        ]
        
        for idx, (text, img, cmd, color) in enumerate(buttons):
            create_button(option_bar, img, text, cmd, color, 0, idx)
        
        return option_bar

    def _create_main_frame(self, parent):
        """Cria o frame principal onde o conteúdo será exibido"""
        main_frame = ctk.CTkFrame(parent, border_width=3, corner_radius=10, fg_color="white")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        return main_frame

    def _create_test_area(self, parent):
        """Cria a área inferior para testar a conexão com o banco de dados"""
        test_area = ctk.CTkFrame(parent)
        test_area.grid_columnconfigure(0, weight=0)
        test_area.grid_columnconfigure(1, weight=1)
        self.label_result = ctk.CTkLabel(test_area, text="")
        self.label_result.grid(row=0, column=1, sticky="nsw", padx=5, pady=5)
        test_button = ctk.CTkButton(test_area, text="Testar Conexão", command=self.test_connection)
        test_button.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)
        return test_area

    def test_connection(self):
        """Executa o teste de conexão e exibe o resultado"""
        show_results(self.label_result)

if __name__ == "__main__":
    app = DispensaApp()
    app.mainloop()
