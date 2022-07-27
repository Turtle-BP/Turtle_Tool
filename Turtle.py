#Importando as bibliotecas 
import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import pymysql

#Importando a página principal 
from Pages.Main_Page import Main_Page
from Pages.App_Details import details


#Função de validão de usar 
def User_verification(username, password, root):
    
    # Criando a conexão com o banco de sql
    connection = pymysql.connect(host='mysqlserver.cnzboqhfvndh.sa-east-1.rds.amazonaws.com',
                                 user='admin',
                                 password='turtle316712',
                                 database='turtle',
                                 cursorclass=pymysql.cursors.DictCursor)

    # Criando o cursor
    c = connection.cursor()

    # Query da password
    Query_Login = "SELECT ID FROM Users WHERE Username = %s AND Password = %s"

    # Execute Login
    result = c.execute(Query_Login, (username, password))
    c.close()
    connection.close()

    # Fazendo as condicionais
    if result == 1:

        root.destroy()

        Main_Page()

    else:
        print("Deu errado")

#Função para o carregamento da página de Login
def Login_Page():
    
    # Criando a página
    Login_root = tk.Tk()
    Login_root.title("Turtle Brand Protection")
    Login_root.geometry('320x300')

    # Carregando a imagem
    load_img = Image.open('Img/horizontal_mono_preto.png').resize((250, 70))

    # Renderizando a imagem
    Img = ImageTk.PhotoImage(load_img)

    # Colocando o imagem dentro do frame
    Img_Label = tk.Label(Login_root, image=Img, width=250, height=80)
    Img_Label.grid(row=1, column=0, sticky="N", columnspan=2, padx=30, pady=30)

    # Colocando Texto de usuário
    User_Text = tk.Label(Login_root, text="Nome de usuário:")
    User_Text.grid(row=2, column=0, padx=5, pady=5)

    # Colocando caixa de texto para entrada do nome de usuário
    User_name = tk.Entry(Login_root)
    User_name.grid(row=2, column=1, padx=5, pady=5)

    # Colocando Texto de senha
    Password_Text = tk.Label(Login_root, text="Senha:")
    Password_Text.grid(row=3, column=0, padx=5, pady=5)

    # Colocando caixa de texto para entrada do nome de usuário
    Password = tk.Entry(Login_root, show="*")
    Password.grid(row=3, column=1, padx=5, pady=5)

    # Colocando botão de Login
    Button_Login = ttk.Button(Login_root, text='Login', width=20,command=lambda: User_verification(User_name.get(), Password.get(), Login_root))
    Button_Login.grid(row=4, column=0, pady=8, padx=8)

    Details_Login = ttk.Button(Login_root, text='App', width=20,command=details)
    Details_Login.grid(row=5, column=0, pady=8, padx=8)

    # Colocando de esqueceu a senha
    Button_Forget = ttk.Button(Login_root, text='Esqueceu a senha', width=20)
    Button_Forget.grid(row=4, column=1, pady=8, padx=8)



    Login_root.mainloop()

#Login_Page()
Main_Page()