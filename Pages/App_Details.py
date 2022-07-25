#Importando as bibliotecas 
import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import git

def git_pull():
    try:
        current = os.getcwd()
        g = git.cmd.Git(current)
        g.pull()

        confirm_page = tk.Tk()
        confirm_page.title("!!!!")
        confirm_page.geometry("100x100")

        confirm_text = tk.Label(confirm_page, text="O aplicativo foi atualizado")
        confirm_text.grid(row=1, column=1, padx=10, pady=10, sticky="N")

        confirm_page.mainloop()
    except:
        pass

def details():
    # Criando a página
    details_page = tk.Tk()
    details_page.title("Turtle Brand Protection")
    details_page.geometry('350x180')

    # Criando as variáveis
    Nome_app = 'Nome: Turtle Tool - Artemis' 
    Versão_app = "Versão atual: 1.1.1"
    ultima = 'última atualização: 25/07/2022'

    #Criando Labelframe 
    Detaisl_Frame = ttk.LabelFrame(details_page, text="Detalhes App")
    Detaisl_Frame.grid(row=1, column=1, padx=10, pady=10)

    #Colocando os pontos 
    Nome_text = ttk.Label(Detaisl_Frame, text=Nome_app)
    Nome_text.grid(row=1, column=1, padx=10, pady=10, sticky="W")

    versao_text = ttk.Label(Detaisl_Frame, text=Versão_app)
    versao_text.grid(row=2, column=1, padx=10, pady=10, sticky="W")

    ultima_text = ttk.Label(Detaisl_Frame, text=ultima)
    ultima_text.grid(row=3, column=1, padx=10, pady=10, sticky="W")

    #Criando o botão 
    Atualize_Button = ttk.Button(details_page, text="Verificar atualização", command=git_pull)
    Atualize_Button.grid(row=1, column=2, padx=10, pady=10)

    details_page.mainloop()



