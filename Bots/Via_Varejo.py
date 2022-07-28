#IMPORTANDO AS BIBLIOTECAS
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm
import pymysql
import json
import os
import random
import requests

from Global_Scripts.Log_Registration import Log

#listas
Urls_Extra = []
Sellers_Extra = []
Country_Extra = []
Price_Extra = []
SKU_Extra = []
Title_Extra = []
Installment_Extra_quantidade = []
Installment_Extra_valor_parcela = []
Installment_Extra_valor_total = []
Prox_pag = []

sellers_name = []
internacional_list = []
sellers_name_correct = []
internacional_name_correct = []


def Via_Varejo_Final(brand,teste_var=None):
    global Selenium_path, options

    def creating_viavarejo_urls(brand,teste_var=None):
        
        if teste_var == None:
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

        #Arrumando espaços vazios
        # Arrumano os espaços vazios
        df['Name'] = df['Name'].str.replace(" ", "-")
        df['Name'] = df['Name'].str.replace("-", "%2B")

        # Criando uma nova coluna no database com a formatação certa
        df['Urls'] = df['Brand'] + "-" + df['Name']

        # Criando a nova coluna que são as urls de pesquisa
        df['Urls_search'] = "https://prd-api-partner.viavarejo.com.br/api/search?resultsPerPage=20&terms=" + df['Brand'][0] + "%2B" + df['Name'] + "&page=1&apiKey=extra&"

        return df

    def search_atributes(url):
        time.sleep(5)
        driver.get(url)
        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        elemento = soup.find('body')

        dic = json.loads(elemento.text)

        # ID
        number_id = 0
        for i in dic['products']:
            try:
                SKU_Extra.append(dic['products'][number_id]['url'])
            except:
                SKU_Extra.append("ERRO")

            number_id = number_id + 1

        # NOME
        number_name = 0
        for i in dic['products']:
            try:
                Title_Extra.append(dic['products'][number_name]['name'])
            except:
                Title_Extra.append("ERRO")

            number_name = number_name + 1

        # SELLER NUMBER
        number_seller = 0
        for i in dic['products']:
            try:
                Sellers_Extra.append(dic['products'][number_seller]['details']['IdLojista'])
            except:
                Sellers_Extra.append("ERRO")

            number_seller = number_seller + 1

        # INTERNACIONAL
        number_internacional = 0
        for i in dic['products']:
            try:
                Country_Extra.append(dic['products'][number_internacional]['details']['categoryName'])
            except:
                Country_Extra.append("ERRO")

            number_internacional = number_internacional + 1

        # PRICE
        number_price = 0
        for i in dic['products']:
            try:
                Price_Extra.append(dic['products'][number_price]['price'])
            except:
                Price_Extra.append("ERRO")

            number_price = number_price + 1

        # INSTALLMENT PARCELA
        number_parcela = 0
        for i in dic['products']:
            try:
                Installment_Extra_quantidade.append(dic['products'][number_parcela]['installment']['count'])
            except:
                Installment_Extra_quantidade.append("ERRO")

            number_parcela = number_parcela + 1

        # INSTALLMENT VALOR PARCELA
        number_valor = 0
        for i in dic['products']:
            try:
                Installment_Extra_valor_parcela.append(dic['products'][number_valor]['installment']['price'])
            except:
                Installment_Extra_valor_parcela.append("ERRO")

            number_valor = number_valor + 1

        # try da próxima página
        try:
            Prox_pag.append(dic['pagination']['next'])
        except:
            pass

    def creating_dataframe(Sellers,Price,Quantidade,SKU,Title,Parcela):
        Dataframe = pd.DataFrame()

        #Colocando Url
        Dataframe['URL'] = SKU

        #Colocando Data
        Dataframe['DATE'] = pd.to_datetime('today', errors='ignore').date()

        Dataframe['MARKETPLACE'] = 'EXTRA'

        correct_seller = []
        #Arrumando sellers
        for seller in Sellers:
            correct_seller.append(seller[0])

        Dataframe['SELLER'] = correct_seller

        Dataframe['PRICE'] = Price

        Dataframe['PARCEL'] = Quantidade
        Dataframe['INSTALLMENT'] = Parcela

        #Criando coluna de Installment_payment
        Dataframe['INSTALLMENT_PAYMENT'] = Dataframe['PARCEL'] * Dataframe['INSTALLMENT']

        Dataframe['ID'] = Dataframe['URL'].str.partition("IdSku=")[2]
        Dataframe['PRODUCT'] = Title

        Dataframe = Dataframe[Dataframe['SELLER'] != "E"]

        #Colocando em ordem
        Dataframe = Dataframe[['DATE','URL','MARKETPLACE','SELLER','PRICE','PARCEL','INSTALLMENT','INSTALLMENT_PAYMENT','ID','PRODUCT']]

        return Dataframe

    def retrieve_sellers(url, sellers):
        #Criando o dataset para retirar as duplicadas
        df_sellers = pd.DataFrame()

        df_sellers['URL'] = url
        df_sellers['SELLER'] = sellers

        #Retirando as duplicadas
        df_sellers.drop_duplicates(subset=['SELLER'], inplace=True)

        return df_sellers

    def get_sellers(url):
        driver = webdriver.Chrome(Selenium_path,options=options)
        driver.get(url)
        time.sleep(5)

        html = driver.page_source

        driver.close()

        Soup = BeautifulSoup(html, 'html.parser')

        try:
            sellers_name.append(Soup.find(class_='e1vg858b0 css-1g8ajdi e1g7zzz30').text)
            try:
                internacional_list.append(Soup.find('img', attrs={'data-testid':'stamps'}))
            except:
                internacional_list.append("NACIONAL")
        except:
            sellers_name.append("ERRO")
            internacional_list.append("ERRO")

    def creating_sellers_dataframe(df_seller, df_final):
        df_seller['Name'] = sellers_name
        df_seller['INTERNACIONAL'] = internacional_list

        #Mudando o nome do seller
        df_seller['Name'] = df_seller['Name'].str.partition("por")[2] 

        for code in df_final['SELLER']:
            sellers_name_correct.append(df_seller.loc[df_seller['SELLER'] == code,'Name'].values[0])

        for code in df_final['SELLER']:
            internacional_name_correct.append(df_seller.loc[df_seller['SELLER'] == code,'INTERNACIONAL'].values[0])

        df_final['Seller_Name'] = sellers_name_correct
        df_final['INTERNACIONAL'] = internacional_name_correct

        return df_final

    #Congiruando o driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.52")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #Pegando o diretório atual
    Current_Dir = os.getcwd()

    #Criando o Path do arquivo de Selenium
    Selenium_path = Current_Dir + "\Data\\ChromeDrivers\\Selenium_103"

    #Abrindo o WebDriver
    driver = webdriver.Chrome(Selenium_path,options=options)

    if teste_var == None:

        Log("SPIDER","Via Varejo",brand,"INICIOU")

        Df_Products = creating_viavarejo_urls(brand)

        for url in tqdm(Df_Products['Urls_search']):
            search_atributes(url)

        Df_ViaVarejo = creating_dataframe(Sellers_Extra,Price_Extra,Installment_Extra_quantidade,SKU_Extra,Title_Extra,Installment_Extra_valor_parcela)

        Sellers_df = retrieve_sellers(Df_ViaVarejo['URL'],Df_ViaVarejo['SELLER'])

        for url in Sellers_df['URL']:
            get_sellers(url)  

        Df_final = creating_sellers_dataframe(Sellers_df,Df_ViaVarejo)

        current_dir = os.getcwd()

        path_download = current_dir + "\Data\\Brands_Downloads\\" + brand + "\ViaVarejo" + brand + ".xlsx"

        Df_final.to_excel(path_download, index=False)

        Log("SPIDER","Via Varejo",brand,"FINALIZOU")

    else:

        Log("SP.TESTE","Via Varejo",brand,"INICIOU")

        Df_Products = creating_viavarejo_urls(brand,teste_var)

        for url in tqdm(Df_Products['Urls_search']):
            search_atributes(url)

        Df_ViaVarejo = creating_dataframe(Sellers_Extra,Price_Extra,Installment_Extra_quantidade,SKU_Extra,Title_Extra,Installment_Extra_valor_parcela)

        Sellers_df = retrieve_sellers(Df_ViaVarejo['URL'],Df_ViaVarejo['SELLER'])

        for url in Sellers_df['URL']:
            get_sellers(url)  

        Df_final = creating_sellers_dataframe(Sellers_df,Df_ViaVarejo)

        current_dir = os.getcwd()

        path_download = current_dir + "\Data\\Brand_Search_Test\\ViaVarejo_" + brand + ".xlsx"

        Df_final.to_excel(path_download, index=False)

        Log("SP.TESTE","Via Varejo",brand,"FINALIZOU")




