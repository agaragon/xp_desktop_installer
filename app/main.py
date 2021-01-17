from selenium import webdriver
from json import load, dumps, loads
from os.path import join
from os import getenv
from sys import path
from tkinter import *
from send_email import send_email
from platform import system
from cryptography.fernet import Fernet
from utils import encode_json_conf
import bs4
import re
import locale
import tkinter.font as font

key = b'1GsKHeGRlS3HcvgCtK5mimWaJBxI2EBDGYAACY9A9TY='

cryptographer = Fernet(key)

if system().lower() == "windows":
        file_name = join(getenv('APPDATA'),'Envia_Email','assets', 'conf')
if system().lower() == "linux":
        file_name = join(path[0], '..','assets', 'conf')

f = open(file_name)

encoded_old_conf = open(file_name, "r")
old_conf_encoded = encoded_old_conf.read().encode()
try:
    conf = loads(cryptographer.decrypt(old_conf_encoded).decode('UTF-8'))
except:
    conf={}
    conf['prospect_link'] = ""

f.close()

root = Tk()

root.title("Clique em configurar para utilizar o seu e-mail")

top_frame = Frame(root)
top_frame.pack()

left_frame = Frame(top_frame)
left_frame.pack(side=LEFT)

right_frame = Frame(top_frame)
right_frame.pack(side=RIGHT)



bottom_frame = Frame(root)
bottom_frame.pack(side=BOTTOM)

def convert_to_reais(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valor = locale.currency(value, grouping=True, symbol=None)
    valor = 'R$' + valor
    return valor

def get_clients_table():
    customers_table = browser.find_element_by_id('table-dashboard-customers')

    if system().lower() == "windows":
        file_name = join(getenv('APPDATA'),'Envia_Email','assets', 'client_info.html')
    if system().lower() == "linux":
        file_name = join(path[0], '..','assets', 'client_info.html')

    f = open(file_name,'w')
    f.write(customers_table.get_attribute('innerHTML'))
    f.close()

def get_client_email_from_html(client_id):
    if system().lower() == "windows":
        file = open(join(getenv('APPDATA'),'Envia_Email','assets', 'client_info.html'))
    if system().lower() == "linux":
        file = open(join(path[0], '..','assets', 'client_info.html'))
    
    # file = open(join(path[0],'..','assets','client_info.html'))
    webpage = file.read()
    soup = bs4.BeautifulSoup(webpage,'html.parser')
    row = soup.find(text=re.compile(f'[^0-9]{client_id}[^0-9]')).parent.parent
    td_list = row.find_all('td')
    file.close()
    return(td_list[4].div.text.strip())

def get_client_name_from_html(client_id):
    if system().lower() == "windows":
        file = open(join(getenv('APPDATA'),'Envia_Email','assets', 'client_info.html'))
    if system().lower() == "linux":
        file = open(join(path[0], '..','assets', 'client_info.html'))
    
    # file = open(join(path[0],'..','assets','client_info.html'))
    webpage = file.read()
    soup = bs4.BeautifulSoup(webpage,'html.parser')
    row = soup.find(text=re.compile(f'[^0-9]{client_id}[^0-9]')).parent.parent
    td_list = row.find_all('td')
    file.close()
    return td_list[1].text.strip()

def save_configuration():

    new_conf_info = {}
    new_sender_email = sender_email_input.get().strip()
    new_offer_name = offer_name_input.get().strip()
    new_link_to_prospect = link_to_prospect_input.get().strip()

    new_value_of_quotes = value_of_quotes_input.get().strip()
    new_value_of_quotes=new_value_of_quotes.strip()
    new_value_of_quotes=new_value_of_quotes.replace('R$','')
    new_value_of_quotes=new_value_of_quotes.replace('.','')
    new_value_of_quotes=new_value_of_quotes.replace(',','.')
    new_email_password = email_password_input.get()

    if not new_sender_email or not new_offer_name or not new_link_to_prospect or not new_value_of_quotes or not new_email_password:
        show_error_window()
    else:
        new_conf_info['email'] = new_sender_email
        new_conf_info['password'] = new_email_password
        new_conf_info['prospect_link'] = new_link_to_prospect
        new_conf_info['value_of_quote'] = new_value_of_quotes
        new_conf_info['offer_name'] = new_offer_name

        user_email_text.set(new_conf_info['email'])

        global conf

        conf = new_conf_info
        encoded_new_conf = encode_json_conf(new_conf_info)
        
        f = open(file_name, 'w')

        f.write(encoded_new_conf)
        f.close()
        new_window.destroy()


def close_new_window():
    new_window.destroy()


def confirm_new_configuration():
    global confirm_new_configuration_window
    confirm_new_configuration_window = Toplevel(new_window)
    confirm_new_configuration_window.title("Confirme a sua configuração:")
    confirm_new_configuration_window.geometry("600x400")
    confirm_new_configuration_window_bottom_frame = Frame(confirm_new_configuration_window)

    close_new_window_btn = Button(new_window_bottom_frame, text="Confirmar",
                                  command=confirm_new_configuration_window.destroy)

def show_error_window():
    global error_window
    error_font = font.Font(family='Helvetica', size=20, weight='bold')

    error_window = Toplevel(new_window)
    error_window.title("Erro de campo vazio")
    error_window.geometry("600x150")
    error_window_bottom_frame = Frame(error_window)
    error_window_label = Label(error_window, text="Todos os campos devem ser preenchidos",pady=40)
    error_window_label['font'] = error_font
    error_window_label.pack(side=TOP)
    close_error_Window_btn = Button(error_window_bottom_frame, text="Fechar",
                                  command=error_window.destroy)

def show_prospect_link():
    global prospect_link_window
    prospect_link_window = Toplevel(new_window)
    prospect_link_window.title("Link do prospecto")
    prospect_link_window.geometry("1200x100")
    prospect_link_window_bottom_frame = Frame(prospect_link_window)
    prospect_link_window_bottom_frame.pack(side=BOTTOM)
    close_prospect_link_window_btn = Button(prospect_link_window_bottom_frame, text="fechar",
                                  command=prospect_link_window.destroy)
    prospect_link_window_label = Label(prospect_link_window, text=f"{conf['prospect_link']}",pady=40)
    prospect_link_window_label.pack(side=TOP)
    close_prospect_link_window_btn.pack(side=BOTTOM)

def open_new_window():
    global new_window

    current_conf_font = font.Font(family='Helvetica', size=15, weight='bold')

    new_window = Toplevel(root)

    new_window.title("Configure seus e-mails:")
    new_window.geometry("600x350")

    new_window_new_conf_label = Label(new_window,text="Nova configuração",pady=5)
    new_window_new_conf_label.pack(side=TOP)
    new_window_new_conf_label['font'] = current_conf_font

    new_window_top_frame = Frame(new_window)
    new_window_top_frame.pack(side=TOP)
    
    new_window_middle_frame = Frame(new_window)
    new_window_middle_frame.pack(side=TOP)

    current_configuration_label = Label(new_window_middle_frame,text="Configuração atual",pady=10)
    current_configuration_label.pack(side=TOP)
    
    current_configuration_label['font'] = current_conf_font

    new_window_middle_left_frame = Frame(new_window_middle_frame)
    new_window_middle_left_frame.pack(side=LEFT)

    new_window_middle_right_frame = Frame(new_window_middle_frame)
    new_window_middle_right_frame.pack(side=RIGHT)

    new_window_left_frame = Frame(new_window_top_frame)
    new_window_left_frame.pack(side=LEFT)

    new_window_right_frame = Frame(new_window_top_frame)
    new_window_right_frame.pack(side=RIGHT)

    new_window_bottom_frame = Frame(new_window)

    save_conf_btn = Button(new_window_bottom_frame, text="Salvar configuração",
                           command=save_configuration)

    close_new_window_btn = Button(new_window_bottom_frame, text="Fechar sem salvar",
                                  command=close_new_window)

    save_table_btn = Button(new_window_bottom_frame, text="Salvar dados",
                           command=get_clients_table)

    open_browser_conf_btn = Button(new_window_bottom_frame, text="Abrir browser",
                           command=open_browser)

    sender_email_label = Label(
        new_window_left_frame, text="Email de quem está enviando:")
    sender_email_label.pack(side=TOP)



    current_email_label = Label(
        new_window_middle_left_frame, text=f"Email de quem está enviando:")
    current_email_label.pack(side=TOP)

    try:
        current_email = conf['email']
    except:
        current_email='Insira seu email'

    current_email_info_label = Label(
        new_window_middle_right_frame, text=current_email)
    current_email_info_label.pack(side=TOP)
    
    current_quote_value_label = Label(
        new_window_middle_left_frame, text=f"Valor de uma cota:")
    current_quote_value_label.pack(side=TOP)
    
    try:
        current_value_of_quotes = convert_to_reais(float(conf['value_of_quote']))
    except:
        current_value_of_quotes='Insira o valor das cotas'

    current_quote_value_info_label = Label(
        new_window_middle_right_frame, text=current_value_of_quotes)
    current_quote_value_info_label.pack(side=TOP)
    
    current_offer_info_label = Label(
        new_window_middle_left_frame, text=f"Nome da oferta:")
    current_offer_info_label.pack(side=TOP)
    
    try:
        current_offer_name  = conf['offer_name']
    except:
        current_offer_name ='Insira um valor para a oferta'

    current_offer_info_label = Label(
        new_window_middle_right_frame, text=current_offer_name)
    current_offer_info_label.pack(side=TOP)
    
    link_to_prospect_label = Label(
        new_window_middle_left_frame, text=f"Link do prospecto:",pady=6)
    link_to_prospect_label.pack(side=TOP)
    
    current_offer_info_label = Button(
        new_window_middle_right_frame, text="Ver link do prospecto",command=show_prospect_link)
    current_offer_info_label.pack(side=TOP)

    global sender_email_input
    sender_email_input = Entry(new_window_right_frame, width=40)
    sender_email_input.pack(side=TOP)

    email_password_label = Label(
        new_window_left_frame, text="Senha do seu e-mail (ela ficará salva de forma segura):")
    email_password_label.pack(side=TOP)

    global email_password_input
    email_password_input = Entry(
        new_window_right_frame, show="*", width=40)
    email_password_input.pack(side=TOP)

    offer_name_label = Label(
        new_window_left_frame, text="Nome da oferta:")
    offer_name_label.pack(side=TOP)

    global offer_name_input
    offer_name_input = Entry(new_window_right_frame, width=40)
    offer_name_input.pack(side=TOP)

    link_to_prospect_label = Label(
        new_window_left_frame, text="Coloque aqui o link do prospecto:")
    link_to_prospect_label.pack(side=TOP)

    global link_to_prospect_input
    link_to_prospect_input = Entry(new_window_right_frame, width=40)
    link_to_prospect_input.pack(side=TOP)

    value_of_quotes_label = Label(
        new_window_left_frame, text="Coloque aqui o valor de uma cota: R$")
    value_of_quotes_label.pack(side=TOP)

    global value_of_quotes_input
    value_of_quotes_input = Entry(new_window_right_frame, width=40)
    value_of_quotes_input.pack(side=TOP)
    
    close_new_window_btn.pack(side=LEFT)
    save_conf_btn.pack(side=LEFT)
    open_browser_conf_btn.pack(side=LEFT)
    save_table_btn.pack(side=LEFT)

    new_window_bottom_frame.pack(side=BOTTOM)
    


def open_browser():
    global browser
    if system().lower() == "windows":
        file_name = join(getenv('APPDATA'),'Envia_Email','assets', 'chromedriver.exe')
    if system().lower() == "linux":
        file_name = join(path[0], '..','assets', 'chromedriver.exe')
    
    # if system().lower() == "windows":
    #     file_name = join(path[0],'..','assets', 'chromedriver.exe')
    #     # destiny_name = join(path[0], 'assets' ,'index_copy.html')
    # if system().lower() == "linux":
    #     file_name = join(path[0], '..','assets', 'chromedriver')
    #     # destiny_name = "file://"+join(path[0], 'assets' ,'index_copy.html')
    destiny_name='https://hub.xpi.com.br/rede/'
    browser = webdriver.Chrome(
        executable_path=file_name)
    browser.get(destiny_name)


def find_table():
    global table_body
    global see_more_btn
    table_body = browser.find_element_by_id('table-dashboard-customers')
    see_more_btn = browser.find_element_by_xpath(
        "//button[contains(text(),'MOSTRAR MAIS')]")


def get_client_info():
    global client_info
    client_info = {}
    client_id = client_id_input.get().strip()
    client_info['id'] = client_id
    client_name_input.insert(END, get_client_name_from_html(client_id))
    client_email_input.insert(END, get_client_email_from_html(client_id))


def get_email_from_trow(trow):
    cells = trow.find_elements_by_tag_name("td")
    email = cells[4].text
    client_info['email'] = email
    return email


def get_name_from_trow(trow):
    cells = trow.find_elements_by_tag_name("td")
    name = cells[1].text
    client_info['name'] = name
    return name


def send_email_to_client():
    client_info['id'] = client_id_input.get().strip()
    client_id_input.delete(0,END)
    client_info['email'] = client_email_input.get().strip()
    client_email_input.delete(0,END)
    client_info['name'] = client_name_input.get().strip()
    client_name_input.delete(0,END)
    client_info['amount_of_quotes'] = str(int(amount_of_quotes_input.get().strip().replace('.','')))
    amount_of_quotes_input.delete(0,END)
    send_email(conf['email'], client_info)


client_id_btn = Button(
    bottom_frame, text="Pegar dados do cliente", command=get_client_info)
send_email_btn = Button(bottom_frame, text="Enviar e-mail",
                        command=send_email_to_client)
open_new_window_btn = Button(bottom_frame, text="Configurar",
                             command=open_new_window)

label_font = font.Font(family='Helvetica', size=12, weight='bold')

user_email_label = Label(left_frame, text="Seu e-mail:")
user_email_label['font'] = label_font
client_id_label = Label(left_frame, text="Id do cliente:")
client_id_label['font'] = label_font
client_name_label = Label(left_frame, text="Nome do cliente:")
client_name_label['font'] = label_font
client_email_label = Label(left_frame, text="Email cliente:")
client_email_label['font'] = label_font
amount_of_quotes_label = Label(
    left_frame, text="Quantidade de cotas:")
amount_of_quotes_label['font'] =label_font


user_email_text = StringVar()
try:
    user_email_text.set(f"{conf['email']}")
except:
    user_email_text.set("Clique em configurar para usar seu email")
user_email_font = font.Font(family='Helvetica', size=12, weight='bold')

user_email_info = Label(right_frame,  textvariable=user_email_text)

user_email_info['font'] = user_email_font



client_id_input = Entry(right_frame, width=40)
client_name_input = Entry(right_frame, width=40)
client_email_input = Entry(right_frame, width=40)
amount_of_quotes_input = Entry(right_frame, width=40)

client_id_btn.pack(side=LEFT)
send_email_btn.pack(side=LEFT)
open_new_window_btn.pack(side=LEFT)

user_email_info.pack(side=TOP,pady=(0,20))

user_email_label.pack(side=TOP,pady=(20,20))
client_id_label.pack(side=TOP,pady=(20,8))
client_name_label.pack(side=TOP,pady=(8,10))
client_email_label.pack(side=TOP,pady=(10,10))
amount_of_quotes_label.pack(side=TOP,pady=(8,10))

client_id_input.pack(side=TOP,pady=(20,10))
client_name_input.pack(side=TOP,pady=(10,10))
client_email_input.pack(side=TOP,pady=(20,10))
amount_of_quotes_input.pack(side=TOP,pady=(20,0))


root.mainloop()
