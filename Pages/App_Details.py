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
        confirm_page.geometry("200x80")

        confirm_text = tk.Label(confirm_page, text="O aplicativo foi atualizado")
        confirm_text.grid(row=1, column=1, padx=10, pady=10, sticky="N")

        confirm_page.mainloop()
    except:
        pass

def updates_registration(root,lista):
    n_row = 0
    for item in lista:
        item_text = ttk.Label(root, text=item)
        item_text.grid(row=n_row, column=1, padx=2, pady=2, sticky="WN")
        n_row = n_row + 1

###3 updatres
updates_list = ["Spider - AliExpress",'Spider - Extra','Spider - Mercado Livre',"Puxar Manual - Estoque","Versão teste - Amazon/Shopee/Kabum","Melhora registros logs"]

def details():
    # Criando a página
    details_page = tk.Tk()
    details_page.title("Turtle Brand Protection")
    details_page.geometry('450x200')

    # Criando as variáveis
    Nome_app = 'Nome: Turtle Tool - Beta' 
    Versão_app = "Versão atual: 1.3.0"
    ultima = 'última atualização: 18/10/2022'

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

    #Colocando as coisas novas 
    Features_n_updates_labelframe = ttk.LabelFrame(details_page, text='Updates')
    Features_n_updates_labelframe.grid(row=1,column=2, padx=10, pady=10, sticky='N')

    updates_registration(Features_n_updates_labelframe,updates_list)

    #Criando o botão 
    Atualize_Button = ttk.Button(details_page, text="Verificar atualização", command=git_pull)
    Atualize_Button.grid(row=2, column=1, padx=10, pady=10, sticky='N')

    details_page.mainloop()



