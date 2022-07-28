#Importando as bibliotecas 
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import NO

import pandas as pd
from PIL import ImageTk, Image

import pymysql

#IMPORTANDO DE GLOBAL SCRIPTS
from Global_Scripts.Menu_Brands import getting_brands
from Pages.Upload_Data import Upload_data
from Pages.Add_Brands import Add_Page
from Pages.Inventory import Inventory_Page
from Pages.Test_Search_Page import Search_Page

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


#################### FUNÇÕES DE SPIDERS ##########################
def Start_AliExpress(marketplace_var, brand):
    #Importando a função
    from Bots.AliExpress import AliExpress_final

    if marketplace_var.get() == "Ligado":

        Ali_Status.config(foreground="orange", text="Buscando")

        Ali_Status.update_idletasks()

        AliExpress_final(brand)

        Ali_Status.config(foreground="green", text="Finalizado")

        Ali_Status.update_idletasks()
    else:
        Ali_Status.config(foreground="red", text="Desativado")



def Start_Amazon(Marketplace_var, brand):
    #Importando a função
    from Bots.Amazon import Amazon_Final

    if Marketplace_var.get() == "Ligado":

        Amazon_Status.config(foreground="orange", text="Buscando")

        Amazon_Status.update_idletasks()

        Amazon_Final(brand)

        Amazon_Status.config(foreground="green", text="Finalizado")

        Amazon_Status.update_idletasks()
    else:
        Amazon_Status.config(foreground="red", text="Desativado")

#def Start_Americanas(Marketplace_var, brand):
    #Importando a função
    #from Spiders.Americanas import americanas_final

    #if Marketplace_var.get() == "Ligado":

        #Americanas_Status.config(foreground="orange", text="Buscando")

        #Americanas_Status.update_idletasks()

        #americanas_final(brand,'padronized')

        #Americanas_Status.config(foreground="green", text="Finalizado")

        #Americanas_Status.update_idletasks()
    #else:
        #Americanas_Status.config(foreground="red", text="Desativado")

#def Start_Carrefour(Marketplace_var, brand):
    #Importando a função
    #from Spiders.Carrefour import carrefour_final

    #if Marketplace_var.get() == "Ligado":

        #Carrefour_Status.config(foreground="orange", text="Buscando")

        #Carrefour_Status.update_idletasks()

        #carrefour_final(brand,'padronized')

        #Carrefour_Status.config(foreground="green", text="Finalizado")

        #Carrefour_Status.update_idletasks()
    #else:
        #Carrefour_Status.config(foreground="red", text="Desativado")

def Start_Extra(Marketplace_var, brand):
    #Importando a função
    from Bots.Via_Varejo import Via_Varejo_Final

    if Marketplace_var.get() == "Ligado":

        Extra_Status.config(foreground="orange", text="Buscando")

        Extra_Status.update_idletasks()

        Via_Varejo_Final(brand)

        Extra_Status.config(foreground="green", text="Finalizado")

        Extra_Status.update_idletasks()
    else:
        Extra_Status.config(foreground="red", text="Desativado")



def Start_Kabum(Marketplace_var, brand):
    #Importando a função
    from Bots.Kabum import Kabum_final

    if Marketplace_var.get() == "Ligado":

        Kabum_Status.config(foreground="orange", text="Buscando")

        Kabum_Status.update_idletasks()

        Kabum_final(brand)

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

        magalu_final(brand)

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

        Shopee_final(brand)

        Shopee_Status.config(foreground="green", text="Finalizado")

        Shopee_Status.update_idletasks()
    else:
        Shopee_Status.config(foreground="red", text="Desativado")

def Start_Spiders(AliExpress,Amazon,Extra,Kabum,Magazine,mercado,shopee, brand_final):
    Start_AliExpress(AliExpress, brand_final)
    Start_Amazon(Amazon, brand_final)
    Start_Extra(Extra, brand_final)
    Start_Magazine(Magazine,brand_final)
    Start_MercadoL(mercado, brand_final)
    Start_Kabum(Kabum,brand_final)
    Start_Shopee(shopee,brand_final)


### FUNÇÕES DE DATA #############
def Logs_records(table):
    global list

    #Conectando com o banco
    connection = pymysql.connect(host='mysqlserver.cnzboqhfvndh.sa-east-1.rds.amazonaws.com',
                             user='admin',
                             password='turtle316712',
                             database='turtle',
                             cursorclass=pymysql.cursors.DictCursor)

    c = connection.cursor()

    c.execute("SELECT * FROM Logs_Scripts")
    result = c.fetchall()
    connection.close()
    c.close()

    log_text = []

    for dictionary in result:
        log_text.append(list(dictionary.values()))

    n = 0
    for list in log_text[-8:]:
        table.insert(parent='',index='end', iid=n, values=list)
        n = n + 1


def Main_Page():

    #DEFININCO OS GLOBAIS NECESSÁRIOS PARA OS SPIDERS
    global Ali_Status,Amazon_Status,Extra_Status,Kabum_Status,Magazine_Status,MercadoL_Status,Shopee_Status

# Criando a página
    Main = tk.Tk()
    Main.title("Turtle Brand Protection - V.1")
    Main.geometry('870x400')

    #Carreando a imagem
    load_img = Image.open('Img/Logo_pequeno.png').resize((30,40))

    #Renderizando a imagem
    Img = ImageTk.PhotoImage(load_img)

    #Colocando a imagem
    Img_label = tk.Label(Main, image=Img, width=30, height=40)
    Img_label.place(x=10,y=10)

    ## ------------ MENU ------------------#
    #Colocando um menu
    Menu_Top_Frame = ttk.LabelFrame(Main)
    Menu_Top_Frame.place(x=60, y=1)

    #Home
    New_Brand_button = ttk.Button(Menu_Top_Frame, text="Databases", command=Add_Page)
    New_Brand_button.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    #Brand Protection
    Upload_Data_button = ttk.Button(Menu_Top_Frame, text="Upload Data", command=Upload_data)
    Upload_Data_button.grid(row=0, column=1, padx=10, pady=10, sticky="W")

    #Brand Protection
    Catalogo_button = ttk.Button(Menu_Top_Frame, text="Catálogo")
    Catalogo_button.grid(row=0, column=2, padx=10, pady=10, sticky="W")

    #Brand Protection
    Inventory_button = ttk.Button(Menu_Top_Frame, text="Inventory", command=Inventory_Page)
    Inventory_button.grid(row=0, column=3, padx=10, pady=10, sticky="W")

    #Brand Protection
    Dashboard_button = ttk.Button(Menu_Top_Frame, text="Dashboard")
    Dashboard_button.grid(row=0, column=4, padx=10, pady=10, sticky="W")

    #Brand Protection
    Search_Urls_button = ttk.Button(Menu_Top_Frame, text="Automatics")
    Search_Urls_button.grid(row=0, column=5, padx=10, pady=10, sticky="W")

    #Brand Protection
    Motorola_Email_button = ttk.Button(Menu_Top_Frame, text="Motorola Email")
    Motorola_Email_button.grid(row=0, column=6, padx=10, pady=10, sticky="W")

    #Brand Protection
    Test_Brand_button = ttk.Button(Menu_Top_Frame, text="Brand Test", command=Search_Page)
    Test_Brand_button.grid(row=0, column=7, padx=10, pady=10, sticky="W")
    ## ------------------------------------#

    ## Spiders ###
    #Criando o LabelFrame
    Menu_Spiders = tk.LabelFrame(Main, text="SPIDERS")
    Menu_Spiders.place(x=450, y=70)

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

    #Utilizando a função
    Brands = list(getting_brands())
    #Criando o Value inside
    Brands_Choice = tk.StringVar(Menu_Spiders)
    # Brands_Choice.set(Brands[0])

    #Criando o elemento de Menu
    Menu_Brand_Element = ttk.OptionMenu(Menu_Spiders, Brands_Choice, *Brands)
    Menu_Brand_Element.grid(row=6, column=1, padx=10, pady=10, sticky="W")

    #Botão para procurar Manual
    Manual_Search_Button = ttk.Button(Menu_Spiders, text="Procura Manual", command=lambda: Start_Spiders(AliVar,AmazonVar,ExtraVar,KabumVar,MagazineVar,MercadoLVar,ShopeeVar,Brands_Choice.get()))
    Manual_Search_Button.grid(row=6, column=2,columnspan=2)

    #Botão para fazer revisão
    Verification_Button = ttk.Button(Menu_Spiders, text="Verificação")
    Verification_Button.grid(row=6, column=3, columnspan=2)

    ## ------------------------------------#


    ## --------------- LOGS ----------------------------------------- #
    #Criando a área de Logs
    Logs_Frame = ttk.LabelFrame(Main, text="Registros")
    Logs_Frame.place(x=15, y=70)

    #Criando a lista
    #Logs_List = tk.Listbox(Logs_Frame, width=62, height=5)
    #Logs_List.grid(row=0, column=0, padx=5, pady=5)
    #Logs_get_data()

    tabela = ttk.Treeview(Logs_Frame)
    tabela.grid(row=0, column=0, padx=5, pady=5)

    tabela['columns'] = ['DATA','HORA','SCRIPT','MARKETPLACE','BRAND','STATUS']
    tabela.column("#0",width=0,stretch=NO)

    tabela.column("DATA",anchor='n',width=60)
    tabela.heading("DATA",text="DATA",anchor='n')
    
    tabela.column("HORA",anchor='n',width=40)
    tabela.heading("HORA",text="HORA",anchor='n')

    tabela.column("SCRIPT",anchor='n',width=50)
    tabela.heading("SCRIPT",text="SCRIPT",anchor='n')

    tabela.column("MARKETPLACE",anchor='n',width=90)
    tabela.heading("MARKETPLACE",text="MARKETPLACE",anchor='n')

    tabela.column("BRAND",anchor='n',width=70)
    tabela.heading("BRAND",text="BRAND",anchor='n')

    tabela.column("STATUS",anchor='n',width=80)
    tabela.heading("STATUS",text="STATUS",anchor='n')

    Logs_records(tabela)


    ## CENTRAL DE AVISOS ##







    Main.mainloop()