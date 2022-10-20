#Importando as bibliotecas
#Importando as bibliotecas
import os

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from requests_html import HTML
from bs4 import BeautifulSoup
from tqdm import tqdm
import pymysql

#Criando as listas vazias
Urls_Amazon = []
Urls_Amazon_More = []
Products_Links = []
Price_Amazon = []
Seller_Amazon = []
Title_Amazon = []
Amazon_installment_price_full = []
More_Offers_List = []
internacional_list = []

#Criando as listas vazias referente aos Button sellers
Seller_Button_Amazon = []
Price_Button_Amazon = []
ASIN_Button_Amazon = []

#Criando as listas vazias referente aos More Sellers
More_Seller_Amazon = []
More_Price_Amazon = []
More_title_Amazon = []
More_ID_Amazon = []

from Global_Scripts.Log_Registration import Log

#Criando a função final
def Amazon_Final(brand, teste_var=None):

    #Criando a função de criar Links
    def Creating_Products_Urls(brand,teste_var=None):
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

            #Passando todos o dataframe para Lowercase
            Dataset_Products = pd.DataFrame()
            Dataset_Products['MARCA'] = [item['Brand'] for item in result]
            Dataset_Products['ITEM'] = [item['Name'] for item in result]
        else:
            Dataset_Products = pd.DataFrame()
            Dataset_Products['ITEM'] = teste_var
            Dataset_Products['MMARCA'] = brand

        #Arrumando os espaços vazios
        Dataset_Products['ITEM'] = Dataset_Products['ITEM'].str.replace(" ","+")

        #Criando as urls
        Dataset_Products['Urls'] = Dataset_Products['MARCA'] + "+" + Dataset_Products['ITEM']

        #Criando a url de pesquisa
        Dataset_Products['Search_Urls'] = "https://www.amazon.com.br/s?k=" + Dataset_Products['Urls']

        #Retornando o df
        return Dataset_Products

    #Criando a função para criar as urls de Search
    def Creating_Search_url(url_search):
        global Urls_Amazon

        time.sleep(5)

        driver.get(url_search)

        time.sleep(5)

        body_el = driver.find_element(By.CSS_SELECTOR, 'body')
        html_str = body_el.get_attribute('innerHTML')
        html_obj = HTML(html=html_str)

        Links = [x for x in html_obj.links]
        products_links = [f'https://www.amazon.com.br{x}' for x in Links]

        for link in products_links:
            Urls_Amazon.append(link)

        Urls_Amazon = [s for s in Urls_Amazon if '/dp/' in s]
        Urls_Amazon = [s for s in Urls_Amazon if not '#customerReviews' in s]

        try:
            Soup = BeautifulSoup(driver.page_source, 'html.parser')
            next_page = "https://www.amazon.com.br" + Soup.find(class_='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator')['href']

            Creating_Search_url(next_page)
        except:
            pass

    #Criando a função para limpar as urls
    def Cleaning_Urls(urls,brand):

        connection = pymysql.connect(host='mysqlserver.cnzboqhfvndh.sa-east-1.rds.amazonaws.com',
                             user='admin',
                             password='turtle316712',
                             database='Products_Brands',
                             cursorclass=pymysql.cursors.DictCursor)

        #Criando o caminho do Databae
        c = connection.cursor()

        #Criando a Query
        Sql_query = "SELECT * FROM Exclusao WHERE Brand = '%s'" % (brand)

        #Conectando com o banco de dados
        c.execute(Sql_query)
        result = c.fetchall()

        #Passando todos o dataframe para Lowercase
        df_itens = pd.DataFrame()
        df_itens['Words'] = [item['Words'] for item in result]

        clean_urls = pd.DataFrame()

        clean_urls['Urls_Completas'] = urls
        clean_urls['Urls_limpas'] = clean_urls['Urls_Completas'].str.partition("ref")[0]

        Urls_limpas = clean_urls['Urls_limpas'].tolist()

        for word in df_itens['Words']:
            Urls_limpas = [s for s in Urls_limpas if not word in s]

        clean_urls = pd.DataFrame()

        clean_urls['Urls_finais'] = Urls_limpas

        clean_urls['ASIN'] = clean_urls['Urls_finais'].str.partition("/dp/")[2].str.partition("/")[0]

        clean_urls.drop_duplicates(subset='ASIN', inplace=True)
        clean_urls.reset_index(inplace=True, drop=True)

        return clean_urls

    #Criando a função para pegar os atributos
    def Search_Atributes(url):
        # Tempo para não haver o bloqueio
        time.sleep(5)

        # Entrando dentro do site com o driver
        driver.get(url)

        # Tempo para carregar
        time.sleep(10)

        body_el = driver.find_element(By.CSS_SELECTOR, 'body')
        html_str = body_el.get_attribute('innerHTML')

        # Criando o Soup
        soup = BeautifulSoup(html_str, 'html.parser')

        # Fazendo o try do nome do vendedor
        try:
            seller = soup.find("a", attrs={"id": 'sellerProfileTriggerId'}).text
            Seller_Amazon.append(seller)
        except:
            Seller_Amazon.append("Erro")

        # Fazendo o try do preço do produto a vista
        try:
            Div_Price = soup.find('div', attrs={"data-feature-name": "corePrice"})
            price = Div_Price.find(class_='a-offscreen').text
            Price_Amazon.append(price)
        except:
            try:
                Price_Amazon.append(soup.find(class_='a-button-text')['href'])
            except:
                Price_Amazon.append("Erro")

        # Pegando o título do produto
        try:
            title = soup.find(id='productTitle').text
            Title_Amazon.append(title)
        except:
            Title_Amazon.append('Erro')

        # Pegando o internacional
        try:
            soup.find('img', attrs={
                'data-a-hires': 'https://images-na.ssl-images-amazon.com/images/G/32/foreignseller/Foreign_Seller_Badge_v2._CB403622375_.png'})
            internacional_list.append("Internacional")
        except:
            internacional_list.append("Nacional")

        # Fazendo o try para pegar o preço da parcela
        try:
            installment = soup.find(class_='best-offer-name a-text-bold').text
            Amazon_installment_price_full.append(installment)
        except:
            Amazon_installment_price_full.append("0")

        # Fazendo o try para ver se tem mais ofertas
        try:
            Main_Div_More_offers = soup.find('div', attrs={"id": "olpLinkWidget_feature_div"})
            Div_More_offers = Main_Div_More_offers.find('div', attrs={'class': 'a-section olp-link-widget'})
            Div_More_offers_text = Div_More_offers.find('div', attrs={'class': 'olp-text-box'}).text
            More_Offers_List.append(Div_More_offers_text)
        except:
            More_Offers_List.append("Comparar outras 0 ofertas")

    #Criando o DataFrame inicial
    def Raw_Dataframe(url, sellers, preco, titulo, installment,  more_url):

        # Criando o DataFrame
        Dataset_amazon = pd.DataFrame()

        # Colocando os dados
        Dataset_amazon['URL'] = url

        Dataset_amazon['DATE'] = pd.to_datetime('today', errors='ignore').date()

        Dataset_amazon['MARKETPLACE'] = "AMAZON"

        # Arrumando a coluna de sellers
        Dataset_amazon['SELLER'] = sellers
        Dataset_amazon['SELLER'] = Dataset_amazon['SELLER'].str.replace("Erro", "Amazon", regex=False)

        # Arrumando o preço
        Dataset_amazon['PRICE'] = preco
        Dataset_amazon['PRICE'] = Dataset_amazon['PRICE'].str.replace(".", "", regex=True)
        Dataset_amazon['PRICE'] = Dataset_amazon['PRICE'].str.replace("R$", "", regex=False)
        Dataset_amazon['PRICE'] = Dataset_amazon['PRICE'].str.replace(",", ".", regex=True)

        # Arrumando os valores de installment
        Dataset_amazon['INSTALLMENT FULL'] = installment
        Dataset_amazon['PARCEL'] = Dataset_amazon['INSTALLMENT FULL'].str.extract('(\d+)')
        Dataset_amazon['PARCEL'] = Dataset_amazon['PARCEL'].astype("int")
        Dataset_amazon['parcel_price_bruto'] = Dataset_amazon['INSTALLMENT FULL'].str.partition("R$")[2].str.partition(" ")[2].str.partition(" ")[0]
        Dataset_amazon['Installment3'] = Dataset_amazon['parcel_price_bruto'].str.extract('(\d+)')
        Dataset_amazon['parcel_price_bruto'] = Dataset_amazon['INSTALLMENT FULL'].str.partition("R$")[2].str.partition(" ")[2].str.partition(" ")[0].str.partition(",")[2]
        Dataset_amazon['Installment4'] = Dataset_amazon['parcel_price_bruto'].str.extract('(\d+)')
        Dataset_amazon['INSTALLMENT'] = Dataset_amazon['Installment3'] + "." + Dataset_amazon['Installment4']
        Dataset_amazon['INSTALLMENT'] = Dataset_amazon['INSTALLMENT'].astype("float")
        Dataset_amazon['INSTALLMENT'] = Dataset_amazon['INSTALLMENT'].fillna(0)
        Dataset_amazon['INSTALLMENT_PAYMENT'] = Dataset_amazon['PARCEL'] * Dataset_amazon['INSTALLMENT']

        Dataset_amazon['ID'] = Dataset_amazon['URL'].str.partition('/dp/')[2].str.partition('/')[0]
        Dataset_amazon['PRODUCT'] = titulo
        Dataset_amazon['INTERNACIONAL'] = internacional_list

        # Arrumando valores de mais sellers
        Dataset_amazon['MORE'] = more_url
        Dataset_amazon['MORE'] = Dataset_amazon['MORE'].str.partition("outras ")[2].str.partition(" ofertas")[0]

        Dataset_amazon['MORE'] = Dataset_amazon['MORE'].astype('int')

        Dataset_amazon = Dataset_amazon.drop(columns=["INSTALLMENT FULL", "Installment3", "Installment4", "parcel_price_bruto"])

        # Colocando na ordem correta
        Dataset_amazon = Dataset_amazon[['DATE', 'URL', 'MARKETPLACE', 'SELLER', 'PRICE', 'PARCEL', 'INSTALLMENT', 'INSTALLMENT_PAYMENT', 'ID','PRODUCT', 'INTERNACIONAL', 'MORE']]

        Dataset_amazon = Dataset_amazon.reset_index(drop=True)

        return Dataset_amazon

    #Criando a função para pegar os sellers de botão
    def Get_Button_Sellers(Dataframe_inicial):
        global Seller_Button_Amazon

        #Fazendo a condicional para pegar apenas os vendedores de botão do dataframe inicial
        Df_Button_Sellers = Dataframe_inicial[Dataframe_inicial['PRICE'].str.len() > 10]

        for id in Df_Button_Sellers['ID']:
            time.sleep(5)

            new_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + id + "&pageno=1&experienceId=aodAjaxMain"

            driver.get(new_url)

            time.sleep(5)

            body_el = driver.find_element(By.CSS_SELECTOR, 'body')
            html_str = body_el.get_attribute('innerHTML')

            Soup = BeautifulSoup(html_str, 'html.parser')

            for seller in Soup.find_all(class_='a-size-small a-color-base'):
                Seller_Button_Amazon.append(seller.text)

            Seller_Button_Amazon = [s for s in Seller_Button_Amazon if not 'avaliações' in s]
            Seller_Button_Amazon = [s for s in Seller_Button_Amazon if not ' Amazon.com.br ' in s]
            Seller_Button_Amazon = [s for s in Seller_Button_Amazon if not 'avaliação' in s]
            Seller_Button_Amazon = [s for s in Seller_Button_Amazon if not 'Recém-lançado' in s]

            for price in Soup.find_all(class_='a-offscreen'):
                Price_Button_Amazon.append(price.text)
                ASIN_Button_Amazon.append(id)

    #Criando a função para criar o DataFrame dos sellers de Button
    def Dataframe_Button(asin, sellers, price, dataframe_final):
        Dataframe_Button = pd.DataFrame()
        Dataframe_Button['ID'] = asin

        Dataframe_Button['DATE'] = pd.to_datetime('today', errors='ignore').date()

        Dataframe_Button['MARKETPLACE'] = 'AMAZON'

        Dataframe_Button['SELLER'] = sellers

        Dataframe_Button['PRICE'] = price
        #Dataframe_Button['PRICE'] = Dataframe_Button['PRICE'].str.replace(".", "", regex=True)
        #Dataframe_Button['PRICE'] = Dataframe_Button['PRICE'].str.replace("R$", "", regex=False)
        #Dataframe_Button['PRICE'] = Dataframe_Button['PRICE'].str.replace(",", ".", regex=True)
        #Dataframe_Button['PRICE'] = Dataframe_Button['PRICE'].astype('float')

        Dataframe_Button['PARCEL'] = 10

        #Dataframe_Button['INSTALLMENT'] = Dataframe_Button['PRICE'] / Dataframe_Button['PARCEL']

        #Dataframe_Button['INSTALLMENT_PAYMENT'] = Dataframe_Button['PRICE'] * Dataframe_Button['PARCEL']

        Dataframe_Button['INTERNACIONAL'] = 'ERRO'

        url_names = []
        for id in Dataframe_Button['ID']:
            url_names.append(dataframe_final.loc[dataframe_final['ID'] == id, 'URL'].values[0])

        products_names = []
        for id in Dataframe_Button['ID']:
            products_names.append(dataframe_final.loc[dataframe_final['ID'] == id, 'PRODUCT'].values[0])

        Dataframe_Button['URL'] = url_names
        Dataframe_Button['PRODUCT'] = products_names

        return Dataframe_Button

    #Função juntar dois dataframe
    def Dataframe_Inicial_With_Button(dataframe_inicial, dataframe_botao):
        dataframe_inicial = dataframe_inicial[dataframe_inicial['PRICE'].str.len() < 10]

        Df_final = pd.concat([dataframe_inicial, dataframe_botao])

        Df_final = Df_final[Df_final['PRICE'] != 'Erro']
        #Df_final['PRICE']= Df_final['PRICE'].astype('float')
        #Df_final = Df_final[Df_final['PRICE'] > 100.99]

        Df_final['MORE'] = Df_final['MORE'].fillna(0.0)
        Df_final['MORE'] = Df_final['MORE'].astype('int')

        return Df_final

    # ------------------- FUNÇÕES PARA PEGAR OS SELLERS DE UM MESMO ANUNCIO ------------------------------------- #
    def search_more_offers_1(ASIN):
        global More_Seller_Amazon

        time.sleep(5)

        new_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + ASIN + "&pageno=1&experienceId=aodAjaxMain"

        driver.get(new_url)

        time.sleep(5)

        body_el = driver.find_element(By.CSS_SELECTOR, 'body')
        html_str = body_el.get_attribute('innerHTML')

        Soup = BeautifulSoup(html_str, 'html.parser')

        for seller in Soup.find_all(class_='a-size-small a-color-base')[4:]:
            More_Seller_Amazon.append(seller.text)

        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'avaliações' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not ' Amazon.com.br ' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'avaliação' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'Recém-lançado' in s]

        for price in Soup.find_all(class_='a-offscreen')[2:]:
            More_Price_Amazon.append(price.text)
            More_ID_Amazon.append(ASIN)

    def search_more_offers_2(ASIN):
        global More_Seller_Amazon

        time.sleep(5)

        new_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + ASIN + "&pageno=2&experienceId=aodAjaxMain"

        driver.get(new_url)

        time.sleep(5)

        body_el = driver.find_element(By.CSS_SELECTOR, 'body')
        html_str = body_el.get_attribute('innerHTML')

        Soup = BeautifulSoup(html_str, 'html.parser')

        for seller in Soup.find_all(class_='a-size-small a-color-base'):
            More_Seller_Amazon.append(seller.text)

        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'avaliações' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not ' Amazon.com.br ' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'avaliação' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'Recém-lançado' in s]

        for price in Soup.find_all(class_='a-offscreen'):
            More_Price_Amazon.append(price.text)
            More_ID_Amazon.append(ASIN)

    def search_more_offers_3(ASIN):
        global More_Seller_Amazon

        time.sleep(5)

        new_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + ASIN + "&pageno=3&experienceId=aodAjaxMain"

        driver.get(new_url)

        time.sleep(5)

        body_el = driver.find_element(By.CSS_SELECTOR, 'body')
        html_str = body_el.get_attribute('innerHTML')

        Soup = BeautifulSoup(html_str, 'html.parser')

        for seller in Soup.find_all(class_='a-size-small a-color-base'):
            More_Seller_Amazon.append(seller.text)

        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'avaliações' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not ' Amazon.com.br ' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'avaliação' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'Recém-lançado' in s]

        for price in Soup.find_all(class_='a-offscreen'):
            More_Price_Amazon.append(price.text)
            More_ID_Amazon.append(ASIN)

    def search_more_offers_4(ASIN):
        global More_Seller_Amazon

        time.sleep(5)

        new_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + ASIN + "&pageno=4&experienceId=aodAjaxMain"

        driver.get(new_url)

        time.sleep(5)

        body_el = driver.find_element(By.CSS_SELECTOR, 'body')
        html_str = body_el.get_attribute('innerHTML')

        Soup = BeautifulSoup(html_str, 'html.parser')

        for seller in Soup.find_all(class_='a-size-small a-color-base'):
            More_Seller_Amazon.append(seller.text)

        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'avaliações' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not ' Amazon.com.br ' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'avaliação' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'Recém-lançado' in s]

        for price in Soup.find_all(class_='a-offscreen'):
            More_Price_Amazon.append(price.text)
            More_ID_Amazon.append(ASIN)

    def search_more_offers_5(ASIN):
        global More_Seller_Amazon

        time.sleep(5)

        new_url = "https://www.amazon.com.br/gp/product/ajax/?asin=" + ASIN + "&pageno=5&experienceId=aodAjaxMain"

        driver.get(new_url)

        time.sleep(5)

        body_el = driver.find_element(By.CSS_SELECTOR, 'body')
        html_str = body_el.get_attribute('innerHTML')

        Soup = BeautifulSoup(html_str, 'html.parser')

        for seller in Soup.find_all(class_='a-size-small a-color-base'):
            More_Seller_Amazon.append(seller.text)

        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'avaliações' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not ' Amazon.com.br ' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'avaliação' in s]
        More_Seller_Amazon = [s for s in More_Seller_Amazon if not 'Recém-lançado' in s]

        for price in Soup.find_all(class_='a-offscreen'):
            More_Price_Amazon.append(price.text)
            More_ID_Amazon.append(ASIN)


    # ----------------------------------------------------------------------------------------------------------- #

    def Creating_Dataframe_More_Sellers(id, seller, price, dataframe_inicial):
        Dataframe_More = pd.DataFrame()
        Dataframe_More['ID'] = id

        Dataframe_More['DATE'] = pd.to_datetime('today', errors='ignore').date()

        Dataframe_More['MARKETPLACE'] = 'AMAZON'

        Dataframe_More['SELLER'] = seller

        Dataframe_More['PRICE'] = price
        Dataframe_More['PRICE'] = Dataframe_More['PRICE'].str.replace(".", "", regex=True)
        Dataframe_More['PRICE'] = Dataframe_More['PRICE'].str.replace("R$", "", regex=False)
        Dataframe_More['PRICE'] = Dataframe_More['PRICE'].str.replace(",", ".", regex=True)
        Dataframe_More['PRICE'] = Dataframe_More['PRICE'].astype('float')

        Dataframe_More['PARCEL'] = 10

        Dataframe_More['INSTALLMENT'] = Dataframe_More['PRICE'] / Dataframe_More['PARCEL']

        Dataframe_More['INSTALLMENT_PAYMENT'] = Dataframe_More['PRICE'] * Dataframe_More['PARCEL']

        Dataframe_More['INTERNACIONAL'] = 'ERRO'

        url_names = []
        for id in Dataframe_More['ID']:
            url_names.append(dataframe_inicial.loc[dataframe_inicial['ID'] == id, 'URL'].values[0])

        products_names = []
        for id in Dataframe_More['ID']:
            products_names.append(dataframe_inicial.loc[dataframe_inicial['ID'] == id, 'PRODUCT'].values[0])

        Dataframe_More['URL'] = url_names
        Dataframe_More['PRODUCT'] = products_names

        return Dataframe_More

    Log('SPIDER','AMAZON',brand,'INICIOU')

    #Configurando o WebDriver
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
    Selenium_path = Current_Dir + "\Data\\ChromeDrivers\\Selenium_105"

    #Abrindo o WebDriver
    driver = webdriver.Chrome(Selenium_path,options=options)

    #Fazendo a condiconal
    if teste_var == None:
        Log('SPIDER','AMAZON',brand,'INICIOU')
        #Fazendo a função de criar urls
        Df_Urls = Creating_Products_Urls(brand)

        #Fazendo a função para pegar os links de produtos
        for url in tqdm(Df_Urls['Search_Urls']):
            Creating_Search_url(url)

        #Limpando as urls
        Clean_Urls = Cleaning_Urls(Urls_Amazon,brand)

        #Pegando os atributos
        for url in tqdm(Clean_Urls['Urls_finais']):
            Search_Atributes(url)

        #Criando o dataframe inicial
        Df_inicial = Raw_Dataframe(Clean_Urls['Urls_finais'], Seller_Amazon, Price_Amazon, Title_Amazon, Amazon_installment_price_full, More_Offers_List)

        #Pegando os sellers de botão
        Get_Button_Sellers(Df_inicial)

        #Criando o DataFrame final
        Button_Dataframe = Dataframe_Button(ASIN_Button_Amazon,Seller_Button_Amazon,Price_Button_Amazon,Df_inicial)

        #Função para carregar os dois dataframe juntos
        Df_final_with_button = Dataframe_Inicial_With_Button(Df_inicial, Button_Dataframe)

        #Pegar apenas os More
        More_Offers_Dataframe = Df_final_with_button[Df_final_with_button['MORE'] != 0]

        # REALIZANDO AS CONDICIONAIS DE MORE SELLERS
        for id, more in zip(More_Offers_Dataframe.ID, More_Offers_Dataframe.MORE):
            if more < 10:
                search_more_offers_1(id)
            elif (more > 10) and (more < 20):
                search_more_offers_1(id)
                search_more_offers_2(id)
            elif (more > 20) and (more < 30):
                search_more_offers_1(id)
                search_more_offers_2(id)
                search_more_offers_3(id)
            elif (more > 30) and (more < 40):
                search_more_offers_1(id)
                search_more_offers_2(id)
                search_more_offers_3(id)
                search_more_offers_4(id)
            elif (more > 40) and (more < 50):
                search_more_offers_1(id)
                search_more_offers_2(id)
                search_more_offers_3(id)
                search_more_offers_4(id)
                search_more_offers_5(id)

        Dataframe_More = Creating_Dataframe_More_Sellers(More_ID_Amazon,More_Seller_Amazon,More_Price_Amazon,Df_inicial)

        Df_final = pd.concat([Df_final_with_button,Dataframe_More])

        Download_path = Current_Dir + "\Data\\Brands_Downloads\\" + brand + "\Amazon_" + brand + ".xlsx"

        Df_final.to_excel(Download_path, index=False)

        Log('SPIDER','AMAZON',brand,'FINALIZOU')
    else:
        Log('SP.TEST','AMAZON',brand,'INICIOU')
        #Fazendo a função de criar urls
        Df_Urls = Creating_Products_Urls(brand,teste_var)

        #Fazendo a função para pegar os links de produtos
        for url in tqdm(Df_Urls['Search_Urls']):
            Creating_Search_url(url)

        #Pegando os atributos
        for url in tqdm(Urls_Amazon):
            Search_Atributes(url)

        #Criando o dataframe inicial
        Df_inicial = Raw_Dataframe(Urls_Amazon, Seller_Amazon, Price_Amazon, Title_Amazon, Amazon_installment_price_full, More_Offers_List)

        #Pegando os sellers de botão
        Get_Button_Sellers(Df_inicial)

        #Criando o DataFrame final
        Button_Dataframe = Dataframe_Button(ASIN_Button_Amazon,Seller_Button_Amazon,Price_Button_Amazon,Df_inicial)

        #Função para carregar os dois dataframe juntos
        Df_final_with_button = Dataframe_Inicial_With_Button(Df_inicial, Button_Dataframe)

        #Pegar apenas os More
        More_Offers_Dataframe = Df_final_with_button[Df_final_with_button['MORE'] != 0]

        # REALIZANDO AS CONDICIONAIS DE MORE SELLERS
        for id, more in zip(More_Offers_Dataframe.ID, More_Offers_Dataframe.MORE):
            if more < 10:
                search_more_offers_1(id)
            elif (more > 10) and (more < 20):
                search_more_offers_1(id)
                search_more_offers_2(id)
            elif (more > 20) and (more < 30):
                search_more_offers_1(id)
                search_more_offers_2(id)
                search_more_offers_3(id)
            elif (more > 30) and (more < 40):
                search_more_offers_1(id)
                search_more_offers_2(id)
                search_more_offers_3(id)
                search_more_offers_4(id)
            elif (more > 40) and (more < 50):
                search_more_offers_1(id)
                search_more_offers_2(id)
                search_more_offers_3(id)
                search_more_offers_4(id)
                search_more_offers_5(id)

        Dataframe_More = Creating_Dataframe_More_Sellers(More_ID_Amazon,More_Seller_Amazon,More_Price_Amazon,Df_inicial)

        Df_final = pd.concat([Df_final_with_button,Dataframe_More])

        Download_path = Current_Dir + "\Data\\Brand_Search_Test\\Amazon_" + brand + ".xlsx"

        Df_final.to_excel(Download_path, index=False)

        Log('SP.TEST','AMAZON',brand,'FINALIZOU')