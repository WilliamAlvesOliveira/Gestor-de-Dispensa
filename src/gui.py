import customtkinter as ctk
import logging
from .controller import show_results, boas_vindas
from .utils import create_button

# Configuração do logging para depuração
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class DispensaApp(ctk.CTk):
    def __init__(self):
        """Inicializa a janela principal do aplicativo"""
        super().__init__()

        self.title("Gerenciador de Dispensa")  # Define o título da janela
        self.geometry('800x400')  # Define o tamanho da janela

        # Criar estrutura da interface
        self.create_widgets()


    def create_widgets(self):
        """Cria e organiza os elementos visuais da interface"""

        # Frame principal que conterá todos os outros elementos
        screen = ctk.CTkFrame(self)
        screen.pack(fill="both", expand=True, padx=10, pady=0)

        # Configuração do layout com grid
        screen.grid_rowconfigure(0, weight=5)  # Barra de opções (botões superiores)
        screen.grid_rowconfigure(1, weight=93) # Área de trabalho principal
        screen.grid_rowconfigure(2, weight=2)  # Área inferior (testes de conexão)
        screen.grid_columnconfigure(0, weight=1)

        # Criar barra de opções (menu superior)
        option_bar = self.create_option_bar(screen)
        option_bar.grid(row=0, column=0, sticky="nsew")

        # Criar o frame principal onde o conteúdo será exibido
        self.main_frame = self.create_main_frame(screen)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Exibir mensagem de boas-vindas
        boas_vindas(self.main_frame)

        # Criar área de teste de conexão
        test_area = self.create_test_area(screen)
        test_area.grid(row=2, column=0, sticky="nsew")


    def create_option_bar(self, parent):
        """Cria a barra superior com os botões de navegação"""
        option_bar = ctk.CTkFrame(parent)

        for i in range(5):
            option_bar.grid_columnconfigure(i, weight=1)

        # Lista de botões com seu respectivo nome, ícone e cor
        buttons = [
            ("Adicionar Item", "assets/imagens/add.png", "green"),
            ("Remover Item", "assets/imagens/remove.png", "red"),
            ("Editar Item", "assets/imagens/edit.png", "blue"),
            ("Mostrar Itens", "assets/imagens/itensList.png", "gray"),
            ("Lista de Compras", "assets/imagens/shopList.png", "gray"),
        ]

        # Criando os botões dinamicamente
        for idx, (text, img, color) in enumerate(buttons):
            create_button(option_bar, img, text, lambda t=text: logging.info(f"{t} clicado"), color, 0, idx)

        return option_bar


    
    def create_main_frame(self, parent):
        """Cria o frame principal onde o conteúdo da aplicação será exibido"""
        main_frame = ctk.CTkFrame(parent, border_width=3, corner_radius=10, fg_color="white")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        return main_frame


    def create_test_area(self, parent):
        """Cria a área inferior onde será testada a conexão com o banco de dados"""
        test_area = ctk.CTkFrame(parent)

        test_area.grid_columnconfigure(0, weight=0) # Coluna do botão
        test_area.grid_columnconfigure(1, weight=1) # Coluna do resultado

        # Label que mostrará o resultado do teste
        self.label_result = ctk.CTkLabel(test_area, text="")
        self.label_result.grid(row=0, column=1, sticky="nsw", padx=5, pady=5)

        # Botão para testar a conexão
        test_button = ctk.CTkButton(test_area, text="Testar Conexão", command=self.test_connection)
        test_button.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)

        return test_area


    def test_connection(self):
        """Executa a função que testa a conexão com o banco de dados e exibe o resultado"""
        show_results(self.label_result)


# Executa o aplicativo se o arquivo for rodado diretamente
if __name__ == "__main__":
    app = DispensaApp()
    app.mainloop()

__all__ = ["app"]
