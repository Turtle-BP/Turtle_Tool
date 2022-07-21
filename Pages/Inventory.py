#Importando as bibliotecas 
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import NO

import pandas as pd
import pymysql

def Inventory_Page():
    Page = tk.Tk()
    Page.title("Turtle Brand Protection - V.1")
    Page.geometry('200x100')

    connection = pymysql.connect(host='mysqlserver.cnzboqhfvndh.sa-east-1.rds.amazonaws.com',
                             user='admin',
                             password='turtle316712',
                             database='turtle',
                             cursorclass=pymysql.cursors.DictCursor)

    c = connection.cursor()

    len_rows = c.execute("SELECT * FROM Inventory")

    c.close()
    connection.close()

    len_text = "número de registros: {}".format(len_rows)

    len_label = ttk.Label(Page, text=len_text)
    len_label.grid(row=1, column=1, columnspan=2,padx=10, pady=10, sticky="W")

    Manual_Push = ttk.Button(Page, text="Puxar Manual")
    Manual_Push.grid(row=2, column=1, padx=5, pady=5, sticky="W")

    Insert_url = ttk.Button(Page, text="Adicionar URL")
    Insert_url.grid(row=2, column=2, padx=5, pady=5, sticky="W")

    Page.mainloop()