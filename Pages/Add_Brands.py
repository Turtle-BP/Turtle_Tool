#Importando as bibliotecas 
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import NO

import pandas as pd

import pymysql
from Global_Scripts.Menu_Brands import getting_brands

#Função para adicionar os dados na TABELA DE VISÃO DE PRODUTOS
def Creating_Labels(root):
    Marcas = list(getting_brands())

    #Conectando com o banco
    connection = pymysql.connect(host='historic-brands.csheuezawnml.sa-east-1.rds.amazonaws.com',
                             user='admin',
                             password='turtle316712',
                             database='Products_Brands',
                             cursorclass=pymysql.cursors.DictCursor)

    connection_historic = pymysql.connect(host='historic-brands.csheuezawnml.sa-east-1.rds.amazonaws.com',
                user='admin',
                password='turtle316712',
                database='Historic_Brands',
                cursorclass=pymysql.cursors.DictCursor)

    c_historic = connection_historic.cursor()
    c = connection.cursor()

    c.execute("SELECT * FROM Products")

    List_Values = []
    for brand in Marcas:
        sql = "SELECT * FROM Products WHERE Brand = %s"        
        List_Values.append(brand)
        List_Values.append(c.execute(sql, brand))
        List_Values.append("ATIVO")           

        sql_query = 'SELECT * FROM %s' % (brand)

        result = c_historic.execute(sql_query)        

        List_Values.append(result)

    #result = c.fetchall()
    connection.close()
    c.close()
    connection_historic.close()
    c_historic.close()

    N = 0 
    b_number = 0
    p_number = 1 
    a_number = 2
    h_number = 3
    for value in List_Values:
        try:
            root.insert(parent='', index='end', iid=N, values=(List_Values[b_number],List_Values[p_number],List_Values[a_number],List_Values[h_number]))
            N = N + 1
            b_number = b_number + 4
            p_number = p_number + 4
            a_number = a_number + 4
            h_number = h_number + 4
        except:
            pass

#Função para adicionar elementos a LISTA DE PRODUTOS
def Add_into_list(data):
    Lista_Products.insert(0, data)
    termos.append(data)

#FUNÇÃO para abrir a janela de SUBIR NOVA MARCA
def Add_brand():
    global Lista_Products

    Add_window = tk.Tk()
    Add_window.title("Turtle Brand Protection - V.1")
    Add_window.geometry('300x200')

    #Nome da marca
    Name_brand_text = ttk.Label(Add_window, text="Nome da Marca")
    Name_brand_text.grid(row=0, column=0, padx=5, pady=5, sticky="W")

    #Campo nome 
    Entry_Brand_Name = ttk.Entry(Add_window)
    Entry_Brand_Name.grid(row=1, column=0, padx=5, pady=5, sticky="W")

    Product_text = ttk.Label(Add_window, text="Escreva os produtos")
    Product_text.grid(row=2, column=0, padx=5, pady=5, sticky="W")

    Name_Product_text = ttk.Entry(Add_window)
    Name_Product_text.grid(row=3, column=0, padx=5, pady=5, sticky="W")

    #botão 
    Add_product_button = ttk.Button(Add_window, text='Adicionar produto', command=lambda: Add_into_list(Name_Product_text.get()))
    Add_product_button.grid(row=4, column=0, padx=10, pady=10, sticky="W")

    #lista 
    Lista_Products = tk.Listbox(Add_window, width=20, height=8)
    Lista_Products.grid(row=0, rowspan=8, column=1, padx=5, pady=5)

    #Subir Brand 
    Upload_brand_button = ttk.Button(Add_window, text="Subir Marca", command=lambda: Upload_Brand(Entry_Brand_Name.get(), termos))
    Upload_brand_button.grid(row=7, column=1, padx=5, pady=5, sticky="N")

    Add_window.mainloop()

#FUNÇÃO DE UPLOAD DE NOVA MARCA NOS BANCOS DE DADOS COM COMMIT
def Upload_Brand(brand_name, lista):
    #Conectando com o banco
    connection_brands = pymysql.connect(host='historic-brands.csheuezawnml.sa-east-1.rds.amazonaws.com',
                             user='admin',
                             password='turtle316712',
                             database='turtle',
                             cursorclass=pymysql.cursors.DictCursor)

    c_brands = connection_brands.cursor()

    sql_brands = "INSERT INTO Brands(Brand_Name) VALUES (%s)"

    c_brands.execute(sql_brands, brand_name)

    connection_brands.commit()
    connection_brands.close()
    c_brands.close()

    #Conectando com o banco
    connection_products = pymysql.connect(host='historic-brands.csheuezawnml.sa-east-1.rds.amazonaws.com',
                             user='admin',
                             password='turtle316712',
                             database='Products_Brands',
                             cursorclass=pymysql.cursors.DictCursor)

    c_products = connection_products.cursor()

    sql_products = "INSERT INTO Products VALUES (%s,%s)"

    for itens in lista:
        c_products.execute(sql_products, (brand_name, itens))

    connection_products.commit()
    connection_products.close()
    c_products.close()

#FUNÇÃO PARA ABRIR JANELA DE SUBIR NOVOS ITENS 
def Add_itens():
    global Lista_Products

    Add_itens_window = tk.Tk()
    Add_itens_window.title("Turtle Brand Protection - V.1")
    Add_itens_window.geometry('300x200')

    #Nome da marca
    Name_brand_text = ttk.Label(Add_itens_window, text="Nome da Marca")
    Name_brand_text.grid(row=0, column=0, padx=5, pady=5, sticky="W")

    Brands = list(getting_brands())
    #Criando o Value inside
    Brands_Choice = tk.StringVar(Add_itens_window)

    #Campo nome 
    Entry_Brand_Name = ttk.OptionMenu(Add_itens_window, Brands_Choice, *Brands)
    Entry_Brand_Name.grid(row=1, column=0, padx=5, pady=5, sticky="W")

    Product_text = ttk.Label(Add_itens_window, text="Escreva os produtos")
    Product_text.grid(row=2, column=0, padx=5, pady=5, sticky="W")

    Name_Product_text = ttk.Entry(Add_itens_window)
    Name_Product_text.grid(row=3, column=0, padx=5, pady=5, sticky="W")

    #botão 
    Add_product_button = ttk.Button(Add_itens_window, text='Adicionar produto', command=lambda: Add_into_list(Name_Product_text.get()))
    Add_product_button.grid(row=4, column=0, padx=10, pady=10, sticky="W")

    #lista 
    Lista_Products = tk.Listbox(Add_itens_window, width=20, height=8)
    Lista_Products.grid(row=0, rowspan=8, column=1, padx=5, pady=5)

    #Subir Brand 
    Upload_brand_button = ttk.Button(Add_itens_window, text="Subir Marca", command=lambda: Upload_Brand(Entry_Brand_Name.get(), termos))
    Upload_brand_button.grid(row=7, column=1, padx=5, pady=5, sticky="N")



    Add_itens_window.mainloop()


def Add_Page():
    global termos
    termos = []

    Page_Add = tk.Tk()
    Page_Add.title("Turtle Brand Protection - V.1")
    Page_Add.geometry('480x200')

    Databases_group = ttk.LabelFrame(Page_Add, text="Databases")
    Databases_group.place(x=20, y=15)

    tabela_marcas = ttk.Treeview(Databases_group, height=6)
    tabela_marcas.grid(row=0, column=0, padx=5, pady=5)

    tabela_marcas['columns'] = ['BRAND','N_PRODUTOS','BANCO_DE_DADOS',"HISTORIC"]
    tabela_marcas.column("#0",width=0, stretch=0)

    tabela_marcas.column("BRAND",width=60, anchor="n")
    tabela_marcas.heading("BRAND",text='BRANDS',anchor="n")

    tabela_marcas.column("N_PRODUTOS",width=90, anchor="n")
    tabela_marcas.heading("N_PRODUTOS",text='PRODUTOS',anchor="n")

    tabela_marcas.column("BANCO_DE_DADOS",width=70, anchor="n")
    tabela_marcas.heading("BANCO_DE_DADOS",text='BANCO',anchor="n")

    tabela_marcas.column("HISTORIC",width=70, anchor="n")
    tabela_marcas.heading("HISTORIC",text='HISTORIC',anchor="n")

    Creating_Labels(tabela_marcas)

    #Criando os botões 
    Add_New_Brand_Button = ttk.Button(Page_Add, text="Adicionar Marcar", command=Add_brand)
    Add_New_Brand_Button.place(x=350, y=24)

    Add_New_itens_Button = ttk.Button(Page_Add, text="Adicionar itens", command=Add_itens)
    Add_New_itens_Button.place(x=350, y=64)

    visualizar_Button = ttk.Button(Page_Add, text="Visualizar dados")
    visualizar_Button.place(x=350, y=104)


    Page_Add.mainloop()
