#Importando as bibliotecas
import os
import pymysql

#Criando a função para pegar todas brands do banco
def getting_brands():
    #Conectando com o banco
    connection = pymysql.connect(host='mysqlserver.cnzboqhfvndh.sa-east-1.rds.amazonaws.com',
                             user='admin',
                             password='turtle316712',
                             database='turtle',
                             cursorclass=pymysql.cursors.DictCursor)

    #Criando o cursor
    C = connection.cursor()

    #Executando o script
    C.execute("SELECT Brand_Name FROM Brands")
    result = C.fetchall()
    C.close()

    lista_brands = [item['Brand_Name'] for item in result]

    return lista_brands
