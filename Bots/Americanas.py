#IMPORTANDO BIBLIOTECAS
from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import pymysql
import time
from tqdm import tqdm
import os
import random

#Importando a função de User Agent
from Global_Scripts.User_agents import Random_user_agents
from Global_Scripts.Log_Registration import Log

Links_Americanas = []
Urls_Americanas = []
Sellers_Americanas = []
Country_Americanas = []
Price_Americanas = []
SKU_Americanas = []
Title_Americanas = []
Installment_Americanas_quantidade = []
Installment_Americanas_valor_parcela = []
Installment_Americanas_valor_total = []
More_offers_americanas = []

def getting_n_creating_americanas(brand):
    connection = pymysql.connect(host='mysqlserver.cnzboqhfvndh.sa-east-1.rds.amazonaws.com',
                                user='admin',
                                password='turtle316712',
                                database='Products_Brands',
                                cursorclass=pymysql.cursors.DictCursor)

    #Criando o caminho do Databae
    c = connection.cursor()

    #Criando a Query
    Sql_query = "SELECT * FROM Products WHERE Brand = '%s'" % (brand)

    #Conectando com o banco de dados
    c.execute(Sql_query)
    result = c.fetchall()
    c.close()
    connection.close()

    #Passando todos o dataframe para Lowercase
    df = pd.DataFrame()
    df['Brand'] = [item['Brand'] for item in result]
    df['Product_Name'] = [item['Name'] for item in result]

    #Arrumando espaços vazios
    # Arrumano os espaços vazios
    df['Product_Name'] = df['Product_Name'].str.replace(" ", "-")

    # Criando uma nova coluna no database com a formatação certa
    df['Urls'] = df['Brand'] + "-" + df['Product_Name']

    # Criando a nova coluna que são as urls de pesquisa
    df['Urls_search'] = "https://www.americanas.com.br/busca/" + df['Urls']

    return df

def search_links(url):
    global Links_Americanas

    time.sleep(15)

    Headers_Choice = Random_user_agents("Americanas")

    response = requests.get(url, headers=Headers_Choice)

    print(response.status_code)
    
    if response.status_code != 200:
        Headers_Choice = Random_user_agents("Americanas")
        response = requests.get(url, headers=Headers_Choice)

    else:
        pass

    html = response.text

    bs = BeautifulSoup(html, 'html.parser')

    for link in bs.find_all("a", href=True):
        Links_Americanas.append("https://www.americanas.com.br" + link['href'])

    Links_Americanas = [s for s in Links_Americanas if 'produto' in s]
    Links_Americanas = [s for s in Links_Americanas if not 'theater' in s]
    Links_Americanas = [s for s in Links_Americanas if 'offerId' in s] 

def search_atributes(url):
    time.sleep(30)

    Headers_Choice = Random_user_agents("Americanas")

    response = requests.get(url, headers=Headers_Choice)

    if response.status_code != 200:
        
        Headers_Choice = Random_user_agents("Americanas")
        response = requests.get(url, headers=Headers_Choice)

    else:
        pass

    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    #Title
    try:
        Title_Americanas.append(soup.find(class_='product-title__Title-sc-1hlrxcw-0 jyetLr').text)
    except:
        Title_Americanas.append("Erro")

    #Preço
    try:
        Price_Americanas.append(soup.find(class_='styles__PriceText-sc-x06r9i-0 dUTOlD priceSales').text)
    except:
        Price_Americanas.append('Erro')

    #Installment
    try:
        Installment_Americanas_valor_parcela.append(soup.find(class_='payment-installment-text__Text-sc-12txe9z-0 bfFyfi').text)
    except:
        Installment_Americanas_valor_parcela.append("Erro")

    #Seller
    try:
        Sellers_Americanas.append(soup.find(class_='offers-box__Wrapper-sc-189v1x3-0 kegaFO').text)
    except:
        Sellers_Americanas.append("Erro")

    #More offers 
    try:
        More_offers_americanas.append(soup.find(class_='more-offers__Touchable-sc-15yqej3-2 hYfNEd')['href'])
    except:
        More_offers_americanas.append("Erro")

def Create_dataframe(url, sellers, price, installment, title):
    df_raw = pd.DataFrame()

    Hoje = pd.to_datetime('today', errors='ignore').date()

    df_raw['URL'] = url

    df_raw['DATE'] = Hoje

    df_raw['MARKETPLACE'] = 'Americanas'

    df_raw['SELLER'] = sellers
    df_raw['SELLER'] = df_raw['SELLER'].str.replace("Este produto é vendido e entregue por ","")
    df_raw['SELLER'] = df_raw['SELLER'].str.replace("Este produto é vendido por ","")
    df_raw['SELLER'] = df_raw['SELLER'].str.partition(".")[0]
    df_raw['SELLER'] = df_raw['SELLER'].str.partition(" e")[0]

    df_raw['PRICE'] = price



    df_raw['PRICE'] = df_raw['PRICE'].str.replace("R$ ", "", regex=False)
    df_raw['PRICE'] = df_raw['PRICE'].str.replace(".","")
    df_raw['PRICE'] = df_raw['PRICE'].str.replace(",",".")



    df_raw['Installment_full'] = installment
    df_raw['PARCEL'] = df_raw['Installment_full'].str.partition('x')[0].str.partition("até ")[2]

    df_raw['INSTALLMENT'] = df_raw['Installment_full'].str.partition("x")[2].str.partition("R$ ")[2]
    df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].str.replace(".","")
    df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].str.replace(",",".")

    df_raw['PRODUCT'] = title

    df_raw['MORE'] = More_offers_americanas


    df_raw['ID'] = df_raw['URL'].str.partition("produto/")[2].str.partition('?')[0]


    #df_raw = df_raw[df_raw['PRICE'] != "Erro"]
    #df_raw['PRICE'] = df_raw['PRICE'].astype('float')

    #df_raw = df_raw[df_raw['PARCEL'] != ""]

    #df_raw['PARCEL'] = df_raw['PARCEL'].astype('int')
    #df_raw['PRICE'] = df_raw['PRICE'].astype('float')

    #df_raw = df_raw[df_raw['PRICE'] < 15000]
    #df_raw = df_raw[df_raw['PRICE'] > 100]

    #df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].astype("float")

    #df_raw['INSTALLMENT_PAYMENT'] = df_raw['PARCEL'] * df_raw['INSTALLMENT']

    #df_raw = df_raw[['DATE', 'URL', 'MARKETPLACE', 'SELLER', 'PRICE', 'PARCEL', 'INSTALLMENT', 'INSTALLMENT_PAYMENT','ID', 'PRODUCT',  'MORE']]

    df_raw = df_raw.drop_duplicates(subset=['ID'])


    return df_raw

def Americana_Final(brand):

    Log("SPIDER","AMERICANAS",brand,"INICIOU")

    #Criando os links 
    Df_Links = getting_n_creating_americanas(brand)

    for url in tqdm(Df_Links['Urls_search']):
        search_links(url)

    for url in tqdm(Links_Americanas):
        search_atributes(url)

    Df_final = Create_dataframe(Links_Americanas, Sellers_Americanas, Price_Americanas, Installment_Americanas_valor_parcela, Title_Americanas)

    current_dir = os.getcwd()

    path_download = current_dir + "\Data\\Brands_Downloads\\" + brand + "\Americanas_" + brand + ".xlsx"

    Df_final.to_excel(path_download, index=False)

    Log("SPIDER","AMERICANAS",brand,"FINALIZOU")

    