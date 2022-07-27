#IMPORTANDO AS BIBLIOTECAS
import pandas as pd
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.request import urlopen
import pymysql
import os
import requests

from Global_Scripts.Log_Registration import Log

#Criando as listas para armazenar os dados
ml_url_base = []
ml_urls = []
ml_price = []
ml_seller = []
ml_installment = []
ml_catalog_id = []
ml_catalog_db = []
ml_idetifaction = []
ml_title = []
ml_internacional = []
lista_identification_url = []

seller_catalog = []
price_catalog = []
installment_catalog = []
link_catalog = []
product_catalog = []

#Função para criar os links de busca
def getting_n_creating_mercadolivre_urls(brand,teste_var=None):
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

    # Criando uma nova coluna no database com a formatação certa
    df['Urls'] = df['Brand'] + "-" + df['Name']

    # Criando a nova coluna que são as urls de pesquisa
    df['Urls_search'] = "https://lista.mercadolivre.com.br/" + df['Urls'] + "_ITEM*CONDITION_2230284_NoIndex_True?#applied_value_name%3DNovo%"

    return df

def search_links(url):
    # Colocando URL commo Global
    global ml_urls

    # Colocando um tempo mínimo de 3 segundos
    time.sleep(3)

    # Fazendo o response
    response = urlopen(url)
    html = response.read()

    # Criando o BeautifulSoup
    BS = BeautifulSoup(html, 'html.parser')

    # Pegando todos os links da página
    for link in BS.find_all("a", href=True):
        ml_urls.append(link['href'])

    # Pegando as próximas páginas
    try:
        next_page_link = BS.find_all(class_='andes-pagination__arrow-title')[-1].text

        # Vendo se na seta está escrito 'Seguinte'
        if next_page_link == 'Seguinte':
            next_url = BS.find_all(class_='andes-pagination__link ui-search-link')[-1]['href']

            # Realizando o loop da função com o link da próxima página
            search_links(next_url)
    except:
        pass

    # Limpando as urls
    ml_urls = [s for s in ml_urls if 'tracking_id' in s]
    ml_urls = [s for s in ml_urls if not 'cabo' in s]
    ml_urls = [s for s in ml_urls if not 'luva' in s]
    ml_urls = [s for s in ml_urls if not 'pontas' in s]
    ml_urls = [s for s in ml_urls if not 'suporte' in s]
    ml_urls = [s for s in ml_urls if not 'caneta' in s]
    ml_urls = [s for s in ml_urls if not 'folha' in s]
    ml_urls = [s for s in ml_urls if not 'controle' in s]
    #ml_urls = [s for s in ml_urls if 'produto' in s]
    #ml_urls = [s for s in ml_urls if 'wacom' in s]

    # Tirando as duplicadas
    ml_urls = list(dict.fromkeys(ml_urls))

def search_attributes(url):
    #Criando tempo
    time.sleep(2)

    #Fazendo o response jh
    response = urlopen(url)
    html = response.read()

    #Criando o soup
    BS = BeautifulSoup(html, 'html.parser')

    #Buscando o preço
    try:
        price = BS.find(class_='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact').text
        ml_price.append(price)
    except:
        ml_price.append("ERRO")

    #Buscando o installment
    try:
        div = BS.find('div',attrs={'class':'ui-pdp-price__subtitles'})
        installment = div.text
        ml_installment.append(installment)
    except:
        installment = BS.find(class_='ui-pdp-color--GREEN ui-pdp-size--MEDIUM ui-pdp-family--REGULAR').text
        ml_installment.append(installment)

    #Catalog
    try:
        catalog = BS.find(class_='ui-pdp-other-sellers__link')['href']
        ml_catalog_id.append(catalog)
    except:
        ml_catalog_id.append("NORMAL")

    #Título
    try:
        title = BS.find(class_='ui-pdp-title')
        ml_title.append(title.text)
    except:
        ml_title.append("Erro")

    #Vendedor
    try:
        seller_link = BS.find(class_='ui-pdp-media__action ui-box-component__action')['href']
    except:
        seller_link = "Erro"

    #Internacional
    try:
        internacional_text = BS.find(class_='ui-pdp-icon ui-pdp-icon--cbt-summary ui-pdp-color--BLUE_700').text
        ml_internacional.append(internacional_text)
    except:
        ml_internacional.append("ERRO")


    try:
        #Entrando na página do vendedor
        response = urlopen(seller_link)
        html = response.read()

        #Criando o soup
        BS = BeautifulSoup(html, 'html.parser')

        #Achando o nome do seller
        seller_name = BS.find(class_='store-info__name').text

        #Append do nome do seller
        ml_seller.append(seller_name)
    except:
        ml_seller.append(seller_link)

def create_dataframe(url,seller,price,installment,catalogo,internacional):
    Dataset = pd.DataFrame()

    Dataset['URL'] = url
    Dataset['DATE'] = pd.to_datetime('today', errors='ignore').date()
    Dataset['PRODUCT'] = ml_title

    Dataset['MARKETPLACE'] = 'MERCADO LIVRE'
    Dataset['SELLER'] = seller

    Dataset['Price'] = price
    Dataset['PRICE_1'] = Dataset['Price'].str.partition("reales")[0]
    Dataset["PRICE_2"] = Dataset["Price"].str.partition(" con")[2].str.partition("centavos")[0].str.partition(" ")[2].str.partition(" centavo")[0]

    Dataset['PRICE'] = Dataset['PRICE_1'] + "," + Dataset['PRICE_2']
    Dataset['PRICE'] = Dataset['PRICE'].str.replace(" ","")

    Dataset['CATALOGO'] = catalogo
    Dataset['INTERNACIONAL'] = internacional

    Dataset['Installment'] = installment

    # Arrumando a coluna de installment
    Dataset['PARCEL'] = Dataset['Installment'].str.partition("x")[0]
    #Dataset['PARCEL'] = Dataset['PARCEL'].str.extract("(\d+)").astype(int)
    Dataset["reais"] = Dataset["Installment"].str.partition("reales")[0].str.partition("x")[2]
    Dataset["moedas"] = Dataset["Installment"].str.partition(" con")[2].str.partition("centavos")[0].str.partition(" ")[2].str.partition(" centavo")[0]
    # Dataset['Installment'] = Dataset['reais'] + "." + Dataset['moedas']

    Dataset['INSTALLMENT'] = Dataset['reais'] + "," + Dataset['moedas']
    Dataset['INSTALLMENT'] = Dataset['INSTALLMENT'].str.replace(" ","")

    #Dataset['Catalog'] = catalogo

    Dataset['ASIN'] = Dataset['URL'].str.partition("/")[2].str.partition("/")[2].str.partition("/")[2].str.partition("-")[0]
    Dataset['ASIN_2'] = Dataset['URL'].str.partition("/")[2].str.partition("/")[2].str.partition("/")[2].str.partition("-")[2].str.partition("-")[0]

    Dataset['ASIN_CORRETO'] = Dataset['ASIN'] + Dataset['ASIN_2']

    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/HUAWEIOFICIAL?brandId=3562",'HUAWEI LOJA OFICIAL')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/MPCEL+MOBILE?brandId=3430",'Mpcel Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/MPCEL+MOBILE?brandId=3562",'MPCEL MOBILE')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/ONOFREELETROSERRA?brandId=2156",'Onofre Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/ZOOM_STORE?brandId=3598",'Zoom Store Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/FASTSHOP+OFICIAL?brandId=942",'Fast Shop Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/MERCADOLIVRE+ELETRONICOS?brandId=2707",'Mercado Livre Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/MERCADOLIVRE+ELETRONICOS?brandId=2707", 'Olist Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://www.mercadolivre.com.br/perfil/OLIST?brandId=866", 'Olist Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://www.mercadolivre.com.br/perfil/OLIST-STORE+PREMIUM?brandId=866",'Olist Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://www.mercadolivre.com.br/perfil/OLIST-STORE+SP?brandId=866", 'Olist Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://www.mercadolivre.com.br/perfil/SUNTEKSTOREBR?brandId=2203",'Suntek Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/SUNTEKSTOREBR?brandId=2203",'Suntek Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/OLIST?brandId=866",'Olist Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/OLIST-STORE+PREMIUM?brandId=866",'Olist Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/OLIST-STORE+SP?brandId=866",'Olist Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/E-SPOT?brandId=4166",'Wacom Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/IBYTE.?brandId=3979",'Ibyte Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/INPOWER+INFO?brandId=1655",'INPOWER Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/PICHAUINFORMATICA?brandId=1436",'Pichau Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/PRIMETEK+COMPUTADORES?brandId=2255",'Primetek Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/VLSTORE+INFORMATICA?brandId=3629", 'Leva Digital Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://www.mercadolivre.com.br/perfil/MIMI2231343?brandId=3396", 'Miranda Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/MIMI2231343?brandId=3396",'Miranda Loja Oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/TUDOABE%C3%87A?brandId=1664",'Tudo à Beça Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://www.mercadolivre.com.br/perfil/OLIST-STORE+BA?brandId=866",'Olist Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://www.mercadolivre.com.br/perfil/OLIST-STORE?brandId=866",'Olist Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://www.mercadolivre.com.br/perfil/E-SPOT?brandId=3574",'E-spot Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/BRING.IT2?brandId=1818",'Bring It Loja oficial')
    Dataset['SELLER'] = Dataset['SELLER'].replace("https://perfil.mercadolivre.com.br/A+P%C3%81GINA?brandId=1256",'A Página Loja oficial')


    Dataset.drop(['ASIN','ASIN_2'], axis=1, inplace=True)

    Dataset = Dataset[['DATE','URL','MARKETPLACE','SELLER','PRICE','PARCEL','INSTALLMENT','ASIN_CORRETO','PRODUCT','CATALOGO','INTERNACIONAL']]
    Dataset = Dataset.drop_duplicates(subset=['SELLER','PRICE','PARCEL','INSTALLMENT','PRODUCT'])
    return Dataset

def search_catalog(url):
    time.sleep(3)
    #Entrando no html
    response = requests.get(url)

    #Pegando o html
    html = response.text

    #Criando o Soup
    Soup = BeautifulSoup(html, 'html.parser')

    produto = Soup.find(class_='ui-pdp-title').text

    #Pegando o preço
    for price in Soup.find_all(class_='andes-money-amount ui-pdp-price__part andes-money-amount--cents-superscript andes-money-amount--compact'):
        price_catalog.append(price.text)

    #Pegando as parcelas
    try:
        for price in Soup.find_all(class_='ui-pdp-family--REGULAR ui-pdp-media__title'):
            installment_catalog.append(price.text)
    except:
        for price in Soup.find_all(class_='ui-pdp-family--REGULAR ui-pdp-media__title'):
            installment_catalog.append(price.text)

    #Pegando os vendedores
    for seller in Soup.find_all(class_='ui-pdp-color--BLUE ui-pdp-family--REGULAR'):
        seller_catalog.append(seller.text)
        link_catalog.append(url)
        product_catalog.append(produto)

    try:
        #Pegando a próxima página


        #Fazendo o try da função com a nova url
        search_catalog(Soup.find(class_='andes-pagination__link', attrs={"title":'Seguinte'})['href'])
        print("Nova página")
    except:
        pass

def create_dataframe_catalog(urls, seller, price, installment, title):
    Catalog_dataframe = pd.DataFrame()

    Catalog_dataframe['URL'] = urls
    Catalog_dataframe['SELLER'] = seller

    Catalog_dataframe['PRICE_BRUTO'] = price
    Catalog_dataframe['PRICE_REAL'] = Catalog_dataframe['PRICE_BRUTO'].str.partition(" reales")[0]
    Catalog_dataframe['PRICE_CENTAVOS'] = Catalog_dataframe['PRICE_BRUTO'].str.partition('con ')[2].str.partition(" centavos")[0]

    Catalog_dataframe['PRICE'] = Catalog_dataframe['PRICE_REAL'] + "," + Catalog_dataframe['PRICE_CENTAVOS']

    Catalog_dataframe['INSTALLMENT_BRUTO'] = installment
    Catalog_dataframe['PARCEL'] = Catalog_dataframe['INSTALLMENT_BRUTO'].str.partition('x')[0]

    Catalog_dataframe['INSTALLMENT_REAL'] = Catalog_dataframe['INSTALLMENT_BRUTO'].str.partition('x ')[2].str.partition(" reales")[0]
    Catalog_dataframe['INSTALLMENT_CENTAVO'] = Catalog_dataframe['INSTALLMENT_BRUTO'].str.partition('con ')[2].str.partition(' centavos')[0]

    Catalog_dataframe['INSTALLMENT'] = Catalog_dataframe['INSTALLMENT_REAL'] + "," + Catalog_dataframe['INSTALLMENT_CENTAVO']

    Catalog_dataframe['DATE'] = pd.to_datetime('today', errors='ignore').date()

    Catalog_dataframe['MARKETPLACE'] = 'MERCADO LIVRE'

    Catalog_dataframe = Catalog_dataframe.drop(columns=['PRICE_BRUTO','PRICE_REAL','PRICE_CENTAVOS','INSTALLMENT_BRUTO','INSTALLMENT_REAL','INSTALLMENT_CENTAVO'])

    Catalog_dataframe['ASIN_CORRETO'] = Catalog_dataframe['URL'].str.partition('/p/')[2].str.partition('/')[0]

    Catalog_dataframe['PRODUCT'] = title

    Catalog_dataframe['CATALOGO'] = 'CATALOGO'

    Catalog_dataframe = Catalog_dataframe[['DATE','URL','MARKETPLACE','SELLER','PRICE','PARCEL','INSTALLMENT','ASIN_CORRETO','PRODUCT','CATALOGO']]

    Catalog_dataframe

def Mercado_Livre_Final(brand,teste_var=None):

    if teste_var == None:
        Log("SPIDER","Mercado L",brand,"INICIOU")

        Df_Raw = getting_n_creating_mercadolivre_urls(brand)

        for url in Df_Raw['Urls_search']:
            search_links(url)

        for url in ml_urls:
            search_attributes(url)

        dataset_mercadolivre_sujo = create_dataframe(ml_urls,ml_seller,ml_price,ml_installment,ml_catalog_id,ml_internacional)

        dataset_catalogo_sem_links = dataset_mercadolivre_sujo[dataset_mercadolivre_sujo['CATALOGO'] != "NORMAL"]

        for url in dataset_catalogo_sem_links['CATALOGO']:
            search_catalog(url)

        dataset_catalogo = create_dataframe_catalog(link_catalog,seller_catalog,price_catalog,installment_catalog,product_catalog)

        dataset_mercadolivre_limpo = dataset_mercadolivre_sujo[dataset_mercadolivre_sujo['CATALOGO'] == 'NORMAL']

        df_final = pd.concat([dataset_catalogo,dataset_mercadolivre_limpo])

        current_dir = os.getcwd()

        path_download = current_dir + "\Data\\Brands_Downloads\\" + brand + "\Mercado_Livre_" + brand + ".xlsx"

        df_final.to_excel(path_download, index=False)

        Log("SPIDER","Mercado L",brand,"FINALIZOU")
    else:
        Log("SP.TEST","Mercado L",brand,"INICIOU")

        Df_Raw = getting_n_creating_mercadolivre_urls(brand)

        for url in Df_Raw['Urls_search']:
            search_links(url)

        for url in ml_urls:
            search_attributes(url)

        dataset_mercadolivre_sujo = create_dataframe(ml_urls,ml_seller,ml_price,ml_installment,ml_catalog_id,ml_internacional)

        dataset_catalogo_sem_links = dataset_mercadolivre_sujo[dataset_mercadolivre_sujo['CATALOGO'] != "NORMAL"]

        for url in dataset_catalogo_sem_links['CATALOGO']:
            search_catalog(url)

        dataset_catalogo = create_dataframe_catalog(link_catalog,seller_catalog,price_catalog,installment_catalog,product_catalog)

        dataset_mercadolivre_limpo = dataset_mercadolivre_sujo[dataset_mercadolivre_sujo['CATALOGO'] == 'NORMAL']

        df_final = pd.concat([dataset_catalogo,dataset_mercadolivre_limpo])

        current_dir = os.getcwd()

        path_download = current_dir + "\Data\\Brand_Search_Test\\MercadoLivre_" + brand + ".xlsx"

        df_final.to_excel(path_download, index=False)

        Log("SP.TEST","Mercado L",brand,"FINALIZOU")


