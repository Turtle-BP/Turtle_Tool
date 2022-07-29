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

from Global_Scripts.Log_Registration import Log

#Listas
Ali_links = []
price_Ali = []
Seller_Ali = []
Title_Ali = []
Internacional_Ali = []
Installment_full_Ali = []

def AliExpress_final(brand, teste_var=None):
    global Ali_links

    def creating_aliexpress_links(brand, teste_var=None):
        if teste_var==None:
            connection = pymysql.connect(host='mysqlserver.cnzboqhfvndh.sa-east-1.rds.amazonaws.com',
                                    user='admin',
                                    password='turtle316712',
                                    database='Products_Brands',
                                    cursorclass=pymysql.cursors.DictCursor)

            #Criando o caminho do Databae
            c = connection.cursor()

            #Criando a Query
            Sql_query = "SELECT * FROM Products WHERE Brand = '%s'" % ('Wacom')

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

        df['Name'] = df['Name'].str.replace(" ","+")
        df['Urls'] = df['Brand'] + "+" + df['Name']

        df['Urls_search'] = "https://pt.aliexpress.com/wholesale?SearchText=" + df['Urls']

        return df

    def getting_links(url):
        time.sleep(5)        
        driver.get(url)
        time.sleep(5)       

        y = 1000
        for timer in range(0,50):
            driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 100
            time.sleep(1)

        time.sleep(5)

        html = driver.page_source

        Soup = BeautifulSoup(html, 'html.parser')

        for a in Soup.find_all("a", href=True):
            Ali_links.append(a['href'])
            print(len(Ali_links))

    def search_atributes(urls):
        for url in urls:
            url_nova = 'https:' + url

            time.sleep(5)

            driver.get(url_nova)
            time.sleep(3)

            html = driver.page_source

            Soup = BeautifulSoup(html, 'html.parser')


            try:
                price_Ali.append(Soup.find(class_='product-price-value').text)
            except:
                price_Ali.append("Erro")

            try:
                Seller_Ali.append(Soup.find(class_='shop-name').text)
            except:
                Seller_Ali.append("Erro")

            try:
                Title_Ali.append(Soup.find(class_='product-title-text').text)
            except:
                Title_Ali.append("Erro")

            try:
                Installment_full_Ali.append(Soup.find(class_='product-installment-wrap').text)
            except:
                Installment_full_Ali.append('Erro')

            try:
                Internacional_Ali.append(Soup.find(class_='dynamic-shipping-line dynamic-shipping-contentLayout').text)
            except:
                Internacional_Ali.append("Erro")

    def creating_dataframe(urls, seller, price, installment, title, internacional):
        #Criação do Dataframe
        Df_Ali = pd.DataFrame()

        Df_Ali['URL'] = urls
        Df_Ali['DATE'] = pd.to_datetime('today', errors='ignore').date()
        Df_Ali['MARKETPLACE'] = 'AliExpress'
        Df_Ali['SELLER'] = seller
        Df_Ali['PRICE'] = price
        Df_Ali['INSTALLMENT'] = installment
        Df_Ali['PRODUCT'] = title
        Df_Ali['INTERNACIONAL'] = internacional


        #Df_Ali = Df_Ali[['DATE', 'URL', 'MARKETPLACE', 'SELLER', 'PRICE', 'PARCEL', 'INSTALLMENT', 'INSTALLMENT_PAYMENT','ID', 'PRODUCT',  'MORE']]
        Df_Ali = Df_Ali[['DATE', 'URL', 'MARKETPLACE', 'SELLER', 'PRICE', 'INSTALLMENT', 'PRODUCT',  'INTERNACIONAL']]

        return Df_Ali

    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument("--log-level=3")
    options.add_argument('--no-sandbox')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #Pegando o diretório atual
    Current_Dir = os.getcwd()

    #Criando o Path do arquivo de Selenium
    Selenium_path = Current_Dir + "\Data\\ChromeDrivers\\Selenium_103"

    #Abrindo o WebDriver
    driver = webdriver.Chrome(Selenium_path,options=options)

    if teste_var==None:

        Log("SPIDER","AliExpress",brand,"INICIOU")
        
        Df_Products = creating_aliexpress_links(brand)

        for url in tqdm(Df_Products['Urls_search']):
            getting_links(url)

        Ali_links = [s for s in Ali_links if '/item/' in s]

        for url in tqdm(Ali_links):
            search_atributes(url)

        Df_Aliexpress = creating_dataframe(Ali_links, Seller_Ali, price_Ali, Installment_full_Ali, Title_Ali, Internacional_Ali)

        current_dir = os.getcwd()

        path_download = current_dir + "\Data\\Brands_Downloads\\" + brand + "\AliExpress_" + brand + ".xlsx"

        Df_Aliexpress.to_excel(path_download, index=False)

        Log("SPIDER","AliExpress",brand,"FINALIZOU")
    else:

        Log("SP.TESTE","AliExpress",brand,"INICIOU")

        Df_Products = creating_aliexpress_links(brand,teste_var)

        for url in tqdm(Df_Products['Urls_search']):
            getting_links(url)

        for url in tqdm(Ali_links):
            search_atributes(url)

        Df_Aliexpress = creating_dataframe(Ali_links, Seller_Ali, price_Ali, Installment_full_Ali, Title_Ali, Internacional_Ali)

        current_dir = os.getcwd()

        path_download = current_dir + "\Data\\Brand_Search_Test\\AliExpress_" + brand + ".xlsx"

        Df_Aliexpress.to_excel(path_download, index=False)
      
        Log("SP.TESTE","AliExpress",brand,"FINALIZOU")


    










# %%
