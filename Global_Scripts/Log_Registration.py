import pymysql
import datetime


def Log(script,marketplace,brand,status):
    # Criando a conexão com o banco de sql
    connection = pymysql.connect(host='historic-brands.csheuezawnml.sa-east-1.rds.amazonaws.com',
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
