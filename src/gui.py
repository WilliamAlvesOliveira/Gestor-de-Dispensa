import customtkinter as ctk #importa a biblioteca tkinter abreviando "ctk"
from .controller import test_database_connection, boas_vindas
from.utils import load_img, create_button
import logging

# Configura o logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def show_results():
    # Função que será chamada ao clicar no botão para testar a conexão
    logging.info("Botão clicado! Tentando conexão...")  #mensagem de depuração
    try:
        result = test_database_connection()  #chama a função test_database_connection()  e armazena o resultado
        app.label_result.configure(text=result) # Atualiza o texto do label com o resultado da conexão
        logging.info("Resultado da conexão: %s", result) #mensagem de depuração com o resultado da conexão
    except Exception as e:
      logging.error("Erro ao tentar conexão", exc_info=True) #mensagem de depuraçãp em caso de erro



# Cria a janela principal da aplicação
app = ctk.CTk()
app.title("Gerenciador de Dispensa") # Define o título da janela
app.geometry('800x400') # Define o tamanho da janela

# Cria o frame geral "screen" que ocupa a janela inteira
screen = ctk.CTkFrame(app)
screen.pack(fill="both", expand=True, padx=10, pady=0)

# Configura o layout do frame "screen" com 1 coluna e 2 linhas
screen.grid_rowconfigure(0,weight=5) #primeira linha com 10% da altura
screen.grid_rowconfigure(1, weight=93) #segunda linha ocupa 88% da altura
screen.grid_rowconfigure(2, weight=2) #terceira linha ocupa 2% da altura
screen.grid_columnconfigure(0, weight=1)

# Frame para os botoes
option_bar = ctk.CTkFrame(screen) #cria a seção main
option_bar.grid(row=0, column=0, sticky="nsew") #sticky faz o preenchimento "nsew=nort south east west"

#configuração grid do frame main screen
option_bar.grid_rowconfigure(0, weight=1) #primeira linha
option_bar.grid_columnconfigure(0, weight=1)
option_bar.grid_columnconfigure(1, weight=1)
option_bar.grid_columnconfigure(2, weight=1)
option_bar.grid_columnconfigure(3, weight=1)
option_bar.grid_columnconfigure(4, weight=1)

#botão adicionar itens
create_button(option_bar, "assets/imagens/add.png", "Adicionar Item", "", "green", 0, 0)

#botão remover itens
create_button(option_bar, "assets/imagens/remove.png", "Remover Item", "", "red", 0, 1)

#bbotão editar item
create_button(option_bar, "assets/imagens/edit.png", "Editar Item", "", "blue", 0, 2)

#botão mostrar items
create_button(option_bar, "assets/imagens/itensList.png", "Mostrar Itens", "", "gray", 0, 3)

#botão lista de compras
create_button(option_bar, "assets/imagens/shopList.png", "Lista de Compras", "", "gray", 0, 4 )

#Frame principal main_frame
main_frame = ctk.CTkFrame(screen, border_width=3, corner_radius=10, fg_color="white") #main frame criado dentro do frame screen
main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

# Ajustar o frame principal para expandir com a tela
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

#renderização da tela principal
main_label = boas_vindas(main_frame)

# Frame inferior para a linha divisória e o botão de teste de conexão (segunda linha)
test_area = ctk.CTkFrame(screen) #cria a area de teste
test_area.grid(row=2, column=0, sticky="nsew") #define a posição dela na tela "screen0"

#configuralção da area de teste
test_area.grid_columnconfigure(0, weight=0) #primeira coluna
test_area.grid_columnconfigure(1,weight=1) #segunda coluna

# Cria um botão para testar a conexão ao banco de dados
testbutton = ctk.CTkButton(test_area, text="testar conexão",command=show_results)
testbutton.grid(row=0, column=0, sticky="nsw", padx=5, pady=5) # A# Posiciona o botão no canto inferior esquerdo

# Cria um label para exibir o resultado da conexão
app.label_result = ctk.CTkLabel(test_area, text="")
app.label_result.grid(row=0, column=1, sticky="nsw", padx=5, pady=5) # Adiciona o label à janela com um espaçamento vertical

# Configura o preenchimento vertical e horizontal para centralizar
test_area.grid_rowconfigure(0, weight=1)

# Inicia o loop principal da janela, mantendo-a aberta
app.mainloop()