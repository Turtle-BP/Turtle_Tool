#Importando as bibliotecas
import pymysql
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import datetime

from requests import request

#Criando a função de pegar todos os dados de Estoque 
#Criando função para enviar e-mail 
def Estoque_Mail():
    email_path = "Estoque.xlsx"

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

    server.login('brandprotection.03@turtlebp.com', 'Five@316712')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Estoque Mercado Livre de Hoje'
    msg['From'] = 'brandprotection01@fivec.com.br'
    msg['body'] = 'Linha 1 \n Linha 2 \n Linha 3'
    recipients = ['kcavalcante@turtlebp.com', 'hfernandes@turtlebp.com']
    msg['To'] = ", ".join(recipients)

    part1 = MIMEBase('application', 'octet-stream')
    part1.set_payload(open(email_path, 'rb').read())
    encoders.encode_base64(part1)
    part1.add_header('Content-Disposition', 'attachment;filename="Motorola_monitoramento.xlsx"')

    msg.attach(part1)
    server.sendmail('brandprotection01@fivec.com.br', recipients, msg.as_string())

#Função Logs 
def Log(script,marketplace,brand,status):
    # Criando a conexão com o banco de sql
    connection = pymysql.connect(host='mysqlserver.cnzboqhfvndh.sa-east-1.rds.amazonaws.com',
                                 user='admin',
                                 password='turtle316712',
                                 database='turtle',
                                 cursorclass=pymysql.cursors.DictCursor)

    #Criando o cursor 
    cursor = connection.cursor()

    data_n_hour = datetime.datetime.now()
    data = "%s/%s/%s" % (data_n_hour.day, data_n_hour.month, data_n_hour.year)
    hour = "%s:%s" % (data_n_hour.hour, data_n_hour.minute)

    #SQL 
    sql_code = 'INSERT INTO Logs_Scripts (DATA, HORA, SCRIPT, MARKETPLACE, BRAND, STATUS) VALUES (%s,%s,%s,%s,%s,%s)'

    #Executando o código em SQL 
    cursor.execute(sql_code, (data, hour,script,marketplace,brand,status))

    #Fechando o database 
    connection.commit()
    cursor.close()
    connection.close()


def Estoque():

    Log("Estoque","ML","GOPRO","INICIOU")

    # Criando a conexão com o banco de sql
    connection = pymysql.connect(host='mysqlserver.cnzboqhfvndh.sa-east-1.rds.amazonaws.com',
                                 user='admin',
                                 password='turtle316712',
                                 database='turtle',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()

    cursor.execute("SELECT Hiperlink FROM Inventory")
    result = cursor.fetchall()
    cursor.close()

    hiperlinks = [item['Hiperlink'] for item in result]
    estoque = []

    #Fazendo o loop 
    for url in hiperlinks:
        time.sleep(1.5)
        try:
            response = urlopen(url)
        except:
            pass

        html = response.read()

        bs = BeautifulSoup(html, 'html.parser')

        try:
            ultimo = bs.find(class_='ui-pdp-color--BLACK ui-pdp-size--MEDIUM ui-pdp-family--SEMIBOLD').text
            estoque.append("1")
        except:
            try:
                quant = bs.find(class_='ui-pdp-buybox__quantity__available').text
                estoque.append(quant)
            except:
                estoque.append("-")

    dataset_estoque = pd.DataFrame()

    dataset_estoque['Estoque'] = estoque

    # Arrumando os valores de estoque
    dataset_estoque['Estoque'] = dataset_estoque['Estoque'].str.replace("(", "")
    dataset_estoque["Estoque"] = dataset_estoque["Estoque"].str.replace(" disponíveis", "")
    dataset_estoque["Estoque"] = dataset_estoque["Estoque"].str.replace(")", "")

    #Download do arquivo 
    current_dir = os.getcwd()
    download_path = current_dir + "/Estoque.xlsx"
    dataset_estoque.to_excel(download_path, index=False)

    #Salvando o Logs dentro do banco 
    Log("Estoque","ML","GOPRO","FINALIZADO")

    #Enviando o E-mail 
    Estoque_Mail()

#Executando o arquivo final 
Estoque()

