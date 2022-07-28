#|Importando a bibliotecas
import tkinter
import tkinter as tk
from tkinter import ttk
import pymysql

#bibliotecas
import pandas as pd
import datetime
import os
import datetime

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#SQL

#Função Universal
from Global_Scripts.Menu_Brands import getting_brands

#Função para inspecionar os dados
def Inspec_data(brand_name):
    #Abrindo os dados
    data = pd.read_excel(r"G:\.shortcut-targets-by-id\1VAK5JIWTmtamcYtBHQGeL7FVwcki0pRp\BRAND PROTECTION\Brand Protection_Daily Report.xlsb", engine='pyxlsb', header=1,convert_float=True)

    #Arrumando a coluna da data
    data['Date'] = pd.TimedeltaIndex(data['Date'], unit='d') + datetime.datetime(1899,12,30)

    #Limpando a primeira linha que é nula
    data = data[1:]

    #Filtrando os dados
    data_filtrada = data[data['Brand'] == brand_name]

    #Pegando apenas as colunas que irei utilizar para a construlão dos dados
    data_filtrada = data_filtrada[['Store - Seller','Week','Date','Part','Store','Seller','Suggested Price','Cash Price','Difference','Porcentage','Installments','Parcel Price','Installment Price','Hiperlink','Item','Store Status','Store Group','From_To - Sellers','1P X 3P','Seller Official?','Cash Price Status','Installment Price Status','Action','Status Ad','Brand','Ad',"Ad's Code",'Item Classification','Cross Border']]

    #Mudando as colunas de Action para corrigir sozinha
    data_filtrada['Action'] = data_filtrada['Action'].str.replace(r'(^.*In Progress.*$)', 'Mercado Livre - Take Down')
    data_filtrada['Action'] = data_filtrada['Action'].str.replace('Send Extrajudicial', 'Extrajudicial Sent')

    data_filtrada.loc[(data_filtrada['Ad'] == 'Catalog')&(data_filtrada['Action'] == 'Mercado Livre - Take Down'),'Action'] = "ML Catalog - Take Down"

    #Limpando os dados
    data_filtrada['Store - Seller'] = data_filtrada['Store - Seller'].str.replace("'","")

    data_filtrada['Seller'] = data_filtrada['Seller'].str.replace("'","")
    data_filtrada['From_To - Sellers'] = data_filtrada['From_To - Sellers'].str.replace("'","")
    data_filtrada['Item Classification'] = data_filtrada['Item Classification'].str.replace("'","")

    #Mostrando os dados
    Shape_Label.config(text="Quantidades de registros: {}".format(int(data_filtrada.shape[0])))
    Minor_Date_Label.config(text="Data (antiga): {}".format(data_filtrada['Date'].min().strftime("%d/%m/%Y")))
    Maior_Date_Label.config(text="Data (Recente): {}".format(data_filtrada['Date'].max().strftime("%d/%m/%Y")))
    Max_Price_Cash_Label.config(text="Maior valor (Cash): {}".format(data_filtrada['Cash Price'].max()))
    Min_Price_Cash_Label.config(text="Menor valor (Cash): {}".format(data_filtrada['Cash Price'].min()))
    Max_Price_Installment_Label.config(text="Maior valor (Installment): {}".format(data_filtrada['Installment Price'].max()))
    Min_Price_Installmnet_Label.config(text="Menor valor (Installment): {}".format(data_filtrada['Installment Price'].min()))


    #Atualizando botão
    Main_Button.config(text='Subir Dados', command=lambda: Upload_to_aws(data_filtrada, brand_name))

#Função para baixar os logs que vai enviar para o banco de dados e salvare 
def Log_registration(dataset, brand):
    current = os.getcwd()

    date = datetime.datetime.now()
    date_right = "%s-%s-%s_%s-%s" % (date.day, date.month, date.year, date.hour, date.minute)

    download = current + "\Data\\Backups_Upload_Data\\Upload_" + brand + "_" + date_right + ".xlsx"

    dataset.to_excel(download, index=False)

#Função para inicar o upload dos dados 
def Upload_to_aws(data, brand):
    Log_registration(data, brand)

    connection = pymysql.connect(host='mysqlserver.cnzboqhfvndh.sa-east-1.rds.amazonaws.com',
                             user='admin',
                             password='turtle316712',
                             database='Historic_Brands',
                             cursorclass=pymysql.cursors.DictCursor)

    c = connection.cursor()

    table_script = 'INSERT INTO %s ' % (brand)

    for i, row in data.iterrows():
        SQL_Script = """(STORE_SELLER, WEEK, DATE, PART, 
                                        PRODUCT, STORE, SELLER, SUGGESTED_PRICE, CASH_PRICE, 
                                        DIFFERENCE, PORCENTAGE, INSTALLMENTS, PARCEL_PRICE, 
                                        INSTALLMENT_PRICE, HIPERLINK, ITEM, STORE_STATUS, 
                                        STORE_GROUP, FROM_TO_SELLERS, PXP, SELLER_OFICIAL, 
                                        CASH_PRICE_STATUS, INSTALLMENT_PRICE_STATUS, ACTION, 
                                        STATUS_AD, BRAND, AD_CODE, ITEM_CLASSIFICATION, CROSS_BORDER) VALUES (%s, %s, %s, %s, 
                                                                                                              %s, %s, %s, %s, 
                                                                                                              %s, %s, %s, %s, 
                                                                                                              %s, %s, %s, %s, 
                                                                                                              %s, %s, %s, %s,
                                                                                                              %s, %s, %s, %s, 
                                                                                                              %s, %s, %s, %s, %s)"""

        full_script = table_script + SQL_Script

        c.execute(full_script, (row['Store - Seller'],row['Week'],
                               row['Date'],row['Part'],row['Item'],row['Store'],
                               row['Seller'],row['Suggested Price'],row['Cash Price'],row['Difference'],row['Porcentage'],
                               row['Installments'],row['Parcel Price'],row['Installment Price'],row['Hiperlink'],row['Item'],
                               row['Store Status'],row['Store Group'],row['From_To - Sellers'],row['1P X 3P'],row['Seller Official?'],
                               row['Cash Price Status'],row['Installment Price Status'],row['Action'],row['Status Ad'],row['Brand'],row["Ad's Code"],
                               row['Item Classification'],row['Cross Border']))

    connection.commit()
    connection.close()
    c.close()


def Upload_data():
    #Definindo variáveis globais
    global Shape_Label,Minor_Date_Label,Maior_Date_Label,Max_Price_Cash_Label,Min_Price_Cash_Label,Max_Price_Installment_Label,Min_Price_Installmnet_Label
    global Main_Button

    Upload_Page = tk.Tk()
    Upload_Page.geometry("290x180")
    Upload_Page.title("Turtle Brand Protection")

    #Utilizando a função
    Brands = list(getting_brands())
    #Criando o Value inside
    Brands_Choice = tkinter.StringVar(Upload_Page)
    Brands_Choice.set(Brands[0])

    #Criando o elemento de Menu
    Menu_Brand_Element = ttk.OptionMenu(Upload_Page, Brands_Choice, *Brands)
    Menu_Brand_Element.grid(row=0, column=1, padx=10, pady=10, sticky="W")

    #Botão para inspeção e posteriormente upload
    Main_Button = ttk.Button(Upload_Page, text="Inspecionar", command=lambda: Inspec_data(Brands_Choice.get()))
    Main_Button.place(x=10,y=40)

    #Criando as Labels referente aos dados
    #Tamanho dos dados
    Shape_Label = ttk.Label(Upload_Page,text="Quantidades de registros: ---")
    Shape_Label.place(x=100,y=10)

    #Data antiga
    Minor_Date_Label = ttk.Label(Upload_Page,text="Data (antiga): --/--/----")
    Minor_Date_Label.place(x=100,y=30)

    #Data recente
    Maior_Date_Label = ttk.Label(Upload_Page,text="Data (Recente): --/--/----")
    Maior_Date_Label.place(x=100,y=50)

    #Data recente
    Max_Price_Cash_Label = ttk.Label(Upload_Page,text="Maior valor (Cash): -----")
    Max_Price_Cash_Label.place(x=100,y=70)

    #Data recente
    Min_Price_Cash_Label = ttk.Label(Upload_Page,text="Menor valor (Cash): -----")
    Min_Price_Cash_Label.place(x=100,y=90)

    #Data recente
    Max_Price_Installment_Label = ttk.Label(Upload_Page,text="Maior valor (Installment): -----")
    Max_Price_Installment_Label.place(x=100,y=110)

    #Data recente
    Min_Price_Installmnet_Label = ttk.Label(Upload_Page,text="Menor valor (Installment): -----")
    Min_Price_Installmnet_Label.place(x=100,y=130)

    Upload_Page.mainloop()

