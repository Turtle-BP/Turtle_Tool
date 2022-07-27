#Importando as bibliotecas 
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import NO
import pymysql
import pandas as pd



####  FUNÇÕES DE ELEMENTOS TKINTER #######
#Função para criar CeckButton
def Create_Checkbutton(Frame_name, Text_value, Variable_Value, grid_row, grid_column):
    CheckButton = ttk.Checkbutton(Frame_name, text=Text_value, variable=Variable_Value, onvalue="Ligado", offvalue="Desligado")
    CheckButton.grid(row=grid_row, column=grid_column, pady=(8,4), padx=10, sticky="W")

    return CheckButton

#Função para criar os textos de status
def Create_Status(Frame_name, Text_value, Color):
    Text_Status = ttk.Label(Frame_name, text=Text_value)
    Text_Status.config(foreground=Color)
    return Text_Status

#Função para adicionar itens a lista 
def add_itens_to_list(brand,data):
    Itens_Listbox.insert(0, data)
    itens_list.append(data)
    brand_name.append(brand)

### Função para criar o dataframe de produtos para depois buscar em cada marketplace 
def Creating_dataframe(brand_list, products_lists):
    Dataset_products = pd.DataFrame()
    Dataset_products['Brand'] = brand_list
    Dataset_products['Products'] = products_lists

    return Dataset_products

def Start_Kabum(Marketplace_var, brand):    
    #Importando a função
    from Bots.Kabum import Kabum_final

    if Marketplace_var.get() == "Ligado":

        Kabum_Status.config(foreground="orange", text="Buscando")

        Kabum_Status.update_idletasks()

        Kabum_final(brand,itens_list)

        Kabum_Status.config(foreground="green", text="Finalizado")

        Kabum_Status.update_idletasks()
    else:
        Kabum_Status.config(foreground="red", text="Desativado")

def Start_Magazine(Marketplace_var, brand):
    #Importando a função
    from Bots.Magalu import magalu_final

    if Marketplace_var.get() == "Ligado":

        Magazine_Status.config(foreground="orange", text="Buscando")

        Magazine_Status.update_idletasks()

        magalu_final(brand, itens_list)

        Magazine_Status.config(foreground="green", text="Finalizado")

        Magazine_Status.update_idletasks()
    else:
        Magazine_Status.config(foreground="red", text="Desativado")

def Start_MercadoL(Marketplace_var, brand):
    #Importando a função
    from Bots.Mercado_livre import Mercado_Livre_Final

    if Marketplace_var.get() == "Ligado":

        MercadoL_Status.config(foreground="orange", text="Buscando")

        MercadoL_Status.update_idletasks()

        Mercado_Livre_Final(brand)

        MercadoL_Status.config(foreground="green", text="Finalizado")

        MercadoL_Status.update_idletasks()
    else:
        MercadoL_Status.config(foreground="red", text="Desativado")

def Start_Shopee(Marketplace_var, brand):
        #Importando a função
    from Bots.Shopee import Shopee_final

    if Marketplace_var.get() == "Ligado":

        Shopee_Status.config(foreground="orange", text="Buscando")

        Shopee_Status.update_idletasks()

        Shopee_final(brand, itens_list)

        Shopee_Status.config(foreground="green", text="Finalizado")

        Shopee_Status.update_idletasks()
    else:
        Shopee_Status.config(foreground="red", text="Desativado")

def Start_Spiders(kabum,magalu,mercado,shopee,brand):
    Start_Kabum(kabum,brand)
    Start_Magazine(magalu, brand)
    Start_MercadoL(mercado, brand)
    Start_Shopee(shopee, brand)




def Search_Page():
    #ATRIBUINDO OS ITENS GLOBAIS 
    global Kabum_Status,Magazine_Status,MercadoL_Status,Shopee_Status

    #Criando a lista de itens universal 
    global itens_list,brand_name, Itens_Listbox
    itens_list = []
    brand_name = []

    Search_Page = tk.Tk()
    Search_Page.title("Turtle Brand Protection - V.1")
    Search_Page.geometry('420x450')

    #Criando o espaço para colocar o nome da marca 
    Brand_Name_text_Label = ttk.Label(Search_Page, text='Escreva o nome da marca')
    Brand_Name_text_Label.grid(row=1, column=1, padx=10, pady=10, sticky="N")

    Brand_Name_Text = ttk.Entry(Search_Page)
    Brand_Name_Text.grid(row=2, column=1, padx=5, pady=0, sticky="N")

    #Criando o espaço para colocar o nome dos itens
    Itens_Name_label = ttk.Label(Search_Page, text='Adiciona os itens da marca')
    Itens_Name_label.grid(row=3, column=1, padx=10, pady=10, sticky="N")

    Itens_Name_entry = ttk.Entry(Search_Page)
    Itens_Name_entry.grid(row=4, column=1, padx=5, pady=0, sticky="N")

    #Criando o botão 
    Add_itens_Button = ttk.Button(Search_Page, text="Adicionar", command=lambda: add_itens_to_list(Brand_Name_Text.get(),Itens_Name_entry.get()))
    Add_itens_Button.grid(row=5, column=1, padx=5, pady=5, sticky='N')

    #Criando o botão 
    Search_Button = ttk.Button(Search_Page, text="Puxar Itens", command=lambda: Start_Spiders(KabumVar,MagazineVar,MercadoL_Status,ShopeeVar,Brand_Name_Text.get()))
    Search_Button.grid(row=6, column=1, padx=5, pady=5, sticky='N')

    #Criando a lista onde irá aparecer os itens adicionados 
    Itens_Listbox = tk.Listbox(Search_Page, width=30, height=15)
    Itens_Listbox.grid(row=1, column=2, rowspan=10, padx=10, pady=10, sticky='N')

    #################### CRIANDO A SELEÇÃO DE SPIDERS #############################################
    #Criando o LabelFrame
    Menu_Spiders = tk.LabelFrame(Search_Page, text="SPIDERS")
    Menu_Spiders.grid(row=7, column=1, columnspan=3, padx=20, pady=20, sticky="W")

    #Buttton de Amazon
    AmazonVar = tk.StringVar(Menu_Spiders, value="Desligado")
    Create_Checkbutton(Menu_Spiders, 'Amazon',AmazonVar,0,1)
    Amazon_Status = Create_Status(Menu_Spiders, 'Desligado','red')
    Amazon_Status.grid(row=1,column=1,pady=(0,10))

    #Buttton de Americanas
    AmericanasVar = tk.StringVar(Menu_Spiders, value="Desligado")
    Create_Checkbutton(Menu_Spiders, 'Americanas',AmericanasVar,0,2)
    Americanas_Status = Create_Status(Menu_Spiders, 'Desligado','red')
    Americanas_Status.grid(row=1,column=2,pady=(0,10))

    #Buttton de Carrefour
    CarrefourVar = tk.StringVar(Menu_Spiders, value="Desligado")
    Create_Checkbutton(Menu_Spiders, 'Carrefour',CarrefourVar,0,3)
    Carrefour_Status = Create_Status(Menu_Spiders, 'Desligado','red')
    Carrefour_Status.grid(row=1,column=3,pady=(0,10))

    #Buttton de Extra
    ExtraVar = tk.StringVar(Menu_Spiders, value="Desligado")
    Create_Checkbutton(Menu_Spiders, 'Extra',ExtraVar,0,4)
    Extra_Status = Create_Status(Menu_Spiders, 'Desligado','red')
    Extra_Status.grid(row=1,column=4,pady=(0,10))

    #Buttton de Kabum
    KabumVar = tk.StringVar(Menu_Spiders, value="Desligado")
    Create_Checkbutton(Menu_Spiders, 'Kabum',KabumVar,2,1)
    Kabum_Status = Create_Status(Menu_Spiders, 'Desligado','red')
    Kabum_Status.grid(row=3,column=1,pady=(0,10))

    #Buttton de Magazine
    MagazineVar = tk.StringVar(Menu_Spiders, value="Desligado")
    Create_Checkbutton(Menu_Spiders, 'Magazine',MagazineVar,2,2)
    Magazine_Status = Create_Status(Menu_Spiders, 'Desligado','red')
    Magazine_Status.grid(row=3,column=2,pady=(0,10))

    #Buttton de Mercado
    MercadoLVar = tk.StringVar(Menu_Spiders, value="Desligado")
    Create_Checkbutton(Menu_Spiders, 'MercadoL',MercadoLVar,2,3)
    MercadoL_Status = Create_Status(Menu_Spiders, 'Desligado','red')
    MercadoL_Status.grid(row=3,column=3,pady=(0,10))

    #Buttton de Shopee
    ShopeeVar = tk.StringVar(Menu_Spiders, value="Desligado")
    Create_Checkbutton(Menu_Spiders, 'Shopee',ShopeeVar,2,4)
    Shopee_Status = Create_Status(Menu_Spiders, 'Desligado','red')
    Shopee_Status.grid(row=3,column=4,pady=(0,10))

    #Buttton de AliExpress
    AliVar = tk.StringVar(Menu_Spiders, value="Desligado")
    Create_Checkbutton(Menu_Spiders, 'AliExpress',AliVar,4,1)
    Ali_Status = Create_Status(Menu_Spiders, 'Desligado','red')
    Ali_Status.grid(row=5,column=1,pady=(0,10))

    Search_Page.mainloop()
