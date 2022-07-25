#Importando as bibliotecas
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from requests_html import HTML
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from tqdm import tqdm
import pymysql
import datetime
import os
import requests
import json

from Global_Scripts.Log_Registration import Log

#listas 
Urls_Shopee = []
Price_Shopee = []
Seller_Shopee = []
Title_Shopee = []
Location_Shopee = []

def Shopee_final(brand):

    #Configurando webdriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    Current_Dir = os.getcwd()

    #Criando o Path do arquivo de Selenium
    Selenium_path = Current_Dir + "\Data\\ChromeDrivers\\Selenium_103"

    #Abrindo o WebDriver
    driver = webdriver.Chrome(Selenium_path,options=options)

    #Função para pegar os links 
    def getting_n_creating_urls(brand):
        
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

        #Passando todos o dataframe para Lowercase
        Dataset_Products = pd.DataFrame()
        Dataset_Products['MARCA'] = [item['Brand'] for item in result]
        Dataset_Products['ITEM'] = [item['Name'] for item in result]


        #Arrumando espaços vazios
        # Arrumano os espaços vazios
        Dataset_Products['ITEM'] = Dataset_Products['ITEM'].str.replace(" ", "%20")

        # Criando uma nova coluna no database com a formatação certa
        Dataset_Products['Urls'] = Dataset_Products['MARCA'] + "%20" + Dataset_Products['ITEM']

        # Criando a nova coluna que são as urls de pesquisa
        Dataset_Products['Urls_search'] = "https://www.shopee.com.br/search?facet=11061449&filters=8&keyword=" + Dataset_Products['Urls']
        return Dataset_Products

    #Função para pegar os links das páginas 
    def getting_links(url):
        time.sleep(3)
        driver.get(url)
        time.sleep(3)

        y = 1000
        for timer in range(0,50):
            driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 100
            time.sleep(1)

        html = driver.page_source

        Soup = BeautifulSoup(html, 'html.parser')

        for a in Soup.find_all("a"):
            Urls_Shopee.append(a['href'])

    #Função para arrumar as urls 
    def clean_links(lista):
        global Urls_limpas
        global Urls_certas

        Urls_limpas = [s for s in lista if '-i.' in s]

        Urls_certas = []
        for url in Urls_limpas:
            Urls_certas.append("https://www.shopee.com.br" + url)

        Urls_certas = list(dict.fromkeys(Urls_certas))

    #Função para pegar atributos 
    def get_attributes(url):
        time.sleep(3)

        driver.get(url)
        time.sleep(5)

        html = driver.page_source

        Soup = BeautifulSoup(html, 'html.parser')

        #Preço
        try:
            Price_Shopee.append(Soup.find(class_='pmmxKx').text)
        except:
            Price_Shopee.append("Erro")

        #SSeller
        try:
            Seller_Shopee.append(Soup.find(class_='_6HeM6T').text)
        except:
            Seller_Shopee.append("Erro")

        #Title
        try:
            Title_Shopee.append(Soup.find(class_='VCNVHn').text)
        except:
            Title_Shopee.append("Erro")

        #Location
        try:
            Location_Shopee.append(Soup.find_all(class_='_3Xk7SJ')[-1].text)
        except:
            Location_Shopee.append("Erro")

    #Função criação de dataframe 
    def creation_dataframe(urls, sellers, price, title, location):
        Dataset = pd.DataFrame()

        Dataset['URL'] = urls
        Dataset['DATE'] = pd.to_datetime('today', errors='ignore').date()
        Dataset['MARKETPLACE'] = 'Shopee'

        Dataset['SELLER'] = sellers

        Dataset['PRICE'] = price
        Dataset['PRICE'] = Dataset['PRICE'].str.partition("R$")[2]
        Dataset['PRICE'] = Dataset['PRICE'].str.replace(".","")
        Dataset['PRICE'] = Dataset['PRICE'].str.replace(",",".")
        #Dataset['PRICE'] = Dataset['PRICE'].astype("float")

        Dataset['PARCEL'] = 6
        #Dataset['INSTALLMENT'] = Dataset['PRICE'] / Dataset['PARCEL']
        Dataset['INSTALLMENT_PAYMENT'] = Dataset['PRICE']

        Dataset['ID'] = Dataset['URL'].str.partition("-i.")[2].str.partition("?")[0]
        Dataset['ID'] = Dataset['ID'].str.partition(".")[2]

        Dataset['PRODUCT'] = title
        Dataset['INTERNACIONAL'] = location

        return Dataset

    Log("SPIDER","SHOPEE",brand,"INICIOU")
   
    df_products = getting_n_creating_urls(brand)

    for url in tqdm(df_products['Urls_search']):
        getting_links(url)

    clean_links(Urls_Shopee)

    for url in tqdm(Urls_certas):
        get_attributes(url)

    Df_final = creation_dataframe(Urls_certas, Seller_Shopee, Price_Shopee, Title_Shopee, Location_Shopee)

    Download_path = Current_Dir + "\Data\\Brands_Downloads\\" + brand + "\Shopee_" + brand + ".xlsx"

    Df_final.to_excel(Download_path, index=False)

    Log("SPIDER","SHOPEE",brand,"FINALIZADO")




