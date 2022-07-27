#Importando as bibliotecas
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
import os
import pymysql
import datetime

#Importando a função de User Agent
from Global_Scripts.User_agents import Random_user_agents
from Global_Scripts.Log_Registration import Log

Links_Kabum = []
Urls_Kabum = []
Sellers_Kabum = []
Country_Kabum = []
Price_Kabum = []
SKU_Kabum = []
Title_Kabum = []
Installment_Kabum_quantidade = []
Installment_Kabum_valor_parcela = []
Installment_Kabum_valor_total = []
teste_values = []



#Função para criar os links de busca
def getting_n_creating_kabum(brand, teste_var=None):
    if teste_var==None:
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
        df['Name'] = [item['Name'] for item in result]
    else:
        df = pd.DataFrame()
        df['Name'] = teste_var
        df['Brand'] = brand
        

    #Passando todo o Dataframe para LowerCase   

    #Arrumando espaços vazios
    # df['Name'] = df['Name'].str.replace(" ", "+")
    # df['Name'] = df['Name'].str.replace("-", "+")

    # Criando uma nova coluna no database com a formatação certa
    df['Urls'] = df['Brand'] + "+" + df['Name']

    # Criando a nova coluna que são as urls de pesquisa
    df['Urls_search'] = "https://www.kabum.com.br/busca?query=" + df['Urls']

    return df

def search_links(url):
    global Links_Kabum

    time.sleep(5)

    Headers_Kabum = Random_user_agents('kabum')
    response = requests.get(url, headers=Headers_Kabum)
    html = response.text

    Soup = BeautifulSoup(html, 'html.parser')

    for a in Soup.find_all("a", href=True):
        Links_Kabum.append("https://www.kabum.com.br" + a['href'])

    Links_Kabum = [s for s in Links_Kabum if 'produto' in s]

def get_attributes(url):
    time.sleep(10)

    Headers_Kabum = Random_user_agents('kabum')
    response = requests.get(url, headers=Headers_Kabum)

    html = response.text

    Soup = BeautifulSoup(html, 'html.parser')

    #Titulo
    try:
        Title_Kabum.append(Soup.find("h1", attrs={'itemprop':'name'}).text)
    except:
        Title_Kabum.append("Erro")

    #Preço
    try:
        Price_Kabum.append(Soup.find("h4", attrs={'itemprop':'price'}).text)
    except:
        Price_Kabum.append("Erro")

    #Seller
    try:
        Sellers_Kabum.append(Soup.find('div', attrs={'id':'blocoValores'}).text)
    except:
        Sellers_Kabum.append("Erro")

    #Installment
    try:
        Installment_Kabum_quantidade.append(Soup.find(class_='cardParcels').text)
    except:
        Installment_Kabum_quantidade.append("Erro")

def dataset_creation(urls, sellers, prices, installments, titles):
    df_raw = pd.DataFrame()

    df_raw['URL'] = urls

    df_raw['DATE'] = pd.to_datetime('today', errors='ignore').date()

    df_raw['MARKETPLACE'] = 'Kabum'

    df_raw['SELLER'] = sellers
    df_raw['SELLER'] = df_raw['SELLER'].str.partition("Vendido e entregue por: ")[2].str.partition(" |")[0]

    df_raw['Installment_lixo'] = installments

    df_raw['PARCEL'] = df_raw['Installment_lixo'].str.partition("x")[0].str.extract('(\d+)')

    df_raw['INSTALLMENT'] = df_raw['Installment_lixo'].str.partition("R$")[2]
    df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].str.partition(" ")[0]
    df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].str.replace(",", ".", regex=True)
    df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].str.replace("\xa0", "", regex=False)

    df_raw['PRODUCT'] = titles

    df_raw['PRICE'] = prices

    # df_raw = df_raw[df_raw['PRICE'] != "Erro"]

    df_raw['PRICE'] = df_raw['PRICE'].str.replace("R$", "", regex=False)
    df_raw['PRICE'] = df_raw['PRICE'].str.replace(".", "", regex=False)
    df_raw['PRICE'] = df_raw['PRICE'].str.replace(",", ".", regex=False)
    df_raw['PRICE'] = df_raw['PRICE'].str.replace("\xa0", "", regex=False)
    # df_raw['PRICE'] = df_raw['PRICE'].astype('float')

    df_raw['ID'] = df_raw['URL'].str.partition("produto/")[2].str.partition("/")[0]

    df_raw = df_raw.drop_duplicates(subset='URL')

    # df_raw['INSTALLMENT'] = df_raw['INSTALLMENT'].astype('float')
    # df_raw['PARCEL'] = df_raw['PARCEL'].astype('int')
    #
    # df_raw['INSTALLMENT_PAYMENT'] = df_raw['PARCEL'] * df_raw['INSTALLMENT']

    # df_raw = df_raw[['DATE', 'URL', 'MARKETPLACE', 'SELLER', 'PRICE', 'PARCEL', 'INSTALLMENT', 'INSTALLMENT_PAYMENT', 'ID','PRODUCT']]

    return df_raw

def Kabum_final(brand, teste_var=None):

    if teste_var==None:

        Log("SPIDER","KABUM",brand,"INICIOU")
        
        df = getting_n_creating_kabum(brand)

        for url in tqdm(df['Urls_search']):
            search_links(url)

        for url in tqdm(Links_Kabum):
            get_attributes(url)

        Dataset_Kabum = dataset_creation(Links_Kabum, Sellers_Kabum, Price_Kabum, Installment_Kabum_quantidade, Title_Kabum)

        current_dir = os.getcwd()

        path_download = current_dir + "\Data\\Brands_Downloads\\" + brand + "\Kabum_" + brand + ".xlsx"

        Dataset_Kabum.to_excel(path_download, index=False)

        Log("SPIDER","KABUM",brand,"FINALIZADO")
    else:
        Log("SP.TEST","KABUM",brand,"INICIOU")
        
        df = getting_n_creating_kabum(brand,teste_var)

        for url in tqdm(df['Urls_search']):
            search_links(url)

        for url in tqdm(Links_Kabum):
            get_attributes(url)

        Dataset_Kabum = dataset_creation(Links_Kabum, Sellers_Kabum, Price_Kabum, Installment_Kabum_quantidade, Title_Kabum)

        current_dir = os.getcwd()

        path_download = current_dir + "\Data\\Brand_Search_Test\\Kabum_" + brand + ".xlsx"

        Dataset_Kabum.to_excel(path_download, index=False)

        Log("SP.TEST","KABUM",brand,"FINALIZADO")