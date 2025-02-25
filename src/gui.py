import customtkinter as ctk #importa a biblioteca tkinter abreviando "ctk"
from .db import connection_test #importação da função para testar a conexão com o db
import logging

# Configura o logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def show_results():
    # Função que será chamada ao clicar no botão para testar a conexão
    logging.info("Botão clicado! Tentando conexão...")  #mensagem de depuração
    try:
        result = connection_test() #chama a função testar_conexao e armazena o resultado
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
screen.grid_rowconfigure(0,weight=98) #primeira linha com 98% da altura
screen.grid_rowconfigure(1, weight=2) #segunda linha ocupa 2% da altura
screen.grid_columnconfigure(0, weight=1)

# Frame inferior para a linha divisória e o botão de teste de conexão (segunda linha)
test_area = ctk.CTkFrame(screen) #cria a area de teste
test_area.grid(row=1, column=0, sticky="nsew") #define a posição dela na tela "screen0"

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