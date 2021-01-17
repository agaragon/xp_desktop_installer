import smtplib
import ssl
from os import getenv
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import base64
import locale
from platform import system
from json import load, loads
from os.path import join
from sys import path
from utils import get_server_from_email
from datetime import datetime
from cryptography.fernet import Fernet

key = b'1GsKHeGRlS3HcvgCtK5mimWaJBxI2EBDGYAACY9A9TY='
cryptographer = Fernet(key)


def convert_to_reais(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    valor = locale.currency(value, grouping=True, symbol=None)
    valor = 'R$' + valor
    return valor


def create_greeting():
    hour = datetime.now().hour
    greeting = ""
    if float(hour) > 0 and float(hour) < 12:
        greeting = "bom dia"
    if float(hour) >= 12 and float(hour) < 18:
        greeting = "boa tarde"
    if float(hour) >= 18 and float(hour) <= 23:
        greeting = "boa noite"
    return greeting


def send_email(sender_address, info):
    if system().lower() == "windows":
        file_name = join(getenv('APPDATA'),'Envia_Email','assets', 'conf')
    if system().lower() == "linux":
        file_name = join(path[0], '..','assets', 'conf')

    # file_name = join(path[0],'..', 'assets', 'conf')
    f = open(file_name)
    encoded_old_conf = open(file_name, "r")
    old_conf_encoded = encoded_old_conf.read().encode()
    conf = loads(cryptographer.decrypt(old_conf_encoded).decode('UTF-8'))

    f.close()

    if system().lower() == "windows":
        image_name = join(getenv('APPDATA'),'Envia_Email','assets', 'thumbnail_manchester.png')
    if system().lower() == "linux":
        image_name = join(path[0], '..','assets', 'thumbnail_manchester.png')

    # image_name = join(path[0],'..', 'assets', 'thumbnail_manchester.png')
    msg = EmailMessage()
    data_uri = base64.b64encode(open(image_name, 'rb').read()).decode('utf-8')
    img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
    msg['Subject'] = conf['offer_name']
    msg['From'] = sender_address
    msg['To'] = info['email']
    message_text = f"""
    <!DOCTYPE html>
    <html>
        <body>
            <p>Olá {info['name']}, {create_greeting()}</p>

            <p>Gostaria de confirmar a reserva de compra no seu código {info['id']} na XP:</p>

            <p>-Oferta: {conf['offer_name']}</p>

            <p>-Quantidade de Cotas: {info['amount_of_quotes']}</p>

            <p>-Valor da cota: {convert_to_reais(float(conf['value_of_quote']))}</p>

            <p>-Valor Financeiro Total: {convert_to_reais(float(conf['value_of_quote'])*float(info['amount_of_quotes']))}</p>

            <p>-Link do Prospecto:</p>
            <a href='{conf['prospect_link']}'>{conf['prospect_link']}</a>
            <p>Aguardo a sua confirmação.</p>

            <p>Abraço</p>

            <b style="font-family:Calibri,Arial,Helvetica,sans-serif;line-height:16px; color:rgb(102,102,102);font-size:12px">Importante:</b>
            {img_tag}
            <p style="font-family:Calibri,Arial,Helvetica,sans-serif;line-height:16px; color:rgb(102,102,102);font-size:11px">
            A Manchester Agentes Autônomos de Investimentos S/S Ltda é uma empresa de agentes autônomos de investimento devidamente registrada na Comissão de Valores Mobiliários (CVM), na forma da Instrução Normativa nº 497/11. A Manchester Agentes Autônomos de Investimentos S/S Ltda. atua no mercado financeiro através da XP Investimentos CCTVM S/A, o que pode ser verificado através do site da CVM (<a href="https://www.gov.br/cvm/pt-br">www.cvm.gov.br</a> > Agentes Autônomos > Relação dos Agentes Autônomos contratados por uma Instituição Financeira > Corretoras > XP Investimentos) ou através do site da ANCORD para escritórios credenciados a partir de outubro de 2012 (<a href="http://www.ancord.org.br/Website_Ancord/index.html">http://www.ancord.org.br/Website_Ancord/index.html</a> > Agentes Autonomos > Consultas) ou através do site da própria XP Investimentos CCTVM S/A (<a href="https://www.xpi.com.br/">www.xpi.com.br</a> > Encontre um escritório > Selecione abaixo o estado e a cidade que deseja pesquisar > Veja a lista dos agentes autônomos). Na forma da legislação da CVM, o agente autônomo de investimento não pode administrar ou gerir o patrimônio de investidores. O agente autônomo é um intermediário e depende da autorização prévia do cliente para realizar operações no mercado financeiro. Esta mensagem, incluindo os seus anexos, contém informações confidenciais destinadas a indivíduo e propósito específicos, sendo protegida por lei. Caso você não seja a pessoa a quem foi dirigida a mensagem, deve apagá-la. É terminantemente proibida a utilização, acesso, cópia ou divulgação não autorizada das informações presentes nesta mensagem. As informações contidas nesta mensagem e em seus anexos são de responsabilidade de seu autor, não representando necessariamente ideias, opiniões, pensamentos ou qualquer forma de posicionamento por parte da Manchester Agentes Autônomos de Investimentos S/S Ltda. O investimento em ações é um investimento de risco e rentabilidade passada não é garantia de rentabilidade futura. Na realização de operações com derivativos existe a possibilidade de perdas superiores aos valores investidos, podendo resultar em significativas perdas patrimoniais. Para informações e dúvidas, favor contatar seu agente de investimentos. Para reclamações, favor contatar a Ouvidoria da XP Investimentos no telefone nº 0800-722-3710.
            </p>

        </body>
    </html>
    """

    plain_text = f"""
    Olá {info['name']}, {create_greeting()}

            Gostaria de confirmar a reserva de compra no seu código {info['id']} na XP:

            -Oferta: {conf['offer_name']}

            -Quantidade de Cotas: {info['amount_of_quotes']}

            -Valor da cota: {convert_to_reais(float(conf['value_of_quote']))}

            -Valor Financeiro Total: {convert_to_reais(float(conf['value_of_quote'])*float(info['amount_of_quotes']))}

            -Link do Prospecto:
            {conf['prospect_link']}
            Aguardo a sua confirmação.

            Abraço

            Importante:
            
            A Manchester Agentes Autônomos de Investimentos S/S Ltda é uma empresa de agentes autônomos de investimento devidamente registrada na Comissão de Valores Mobiliários (CVM), na forma da Instrução Normativa nº 497/11. A Manchester Agentes Autônomos de Investimentos S/S Ltda. atua no mercado financeiro através da XP Investimentos CCTVM S/A, o que pode ser verificado através do site da CVM (www.cvm.gov.br > Agentes Autônomos > Relação dos Agentes Autônomos contratados por uma Instituição Financeira > Corretoras > XP Investimentos) ou através do site da ANCORD para escritórios credenciados a partir de outubro de 2012 (http://www.ancord.org.br/Website_Ancord/index.html> Agentes Autonomos > Consultas) ou através do site da própria XP Investimentos CCTVM S/A (www.xpi.com.br > Encontre um escritório > Selecione abaixo o estado e a cidade que deseja pesquisar > Veja a lista dos agentes autônomos). Na forma da legislação da CVM, o agente autônomo de investimento não pode administrar ou gerir o patrimônio de investidores. O agente autônomo é um intermediário e depende da autorização prévia do cliente para realizar operações no mercado financeiro. Esta mensagem, incluindo os seus anexos, contém informações confidenciais destinadas a indivíduo e propósito específicos, sendo protegida por lei. Caso você não seja a pessoa a quem foi dirigida a mensagem, deve apagá-la. É terminantemente proibida a utilização, acesso, cópia ou divulgação não autorizada das informações presentes nesta mensagem. As informações contidas nesta mensagem e em seus anexos são de responsabilidade de seu autor, não representando necessariamente ideias, opiniões, pensamentos ou qualquer forma de posicionamento por parte da Manchester Agentes Autônomos de Investimentos S/S Ltda. O investimento em ações é um investimento de risco e rentabilidade passada não é garantia de rentabilidade futura. Na realização de operações com derivativos existe a possibilidade de perdas superiores aos valores investidos, podendo resultar em significativas perdas patrimoniais. Para informações e dúvidas, favor contatar seu agente de investimentos. Para reclamações, favor contatar a Ouvidoria da XP Investimentos no telefone nº 0800-722-3710.

    """
    msg.set_content(plain_text)
    msg.add_alternative(message_text, subtype="html")

    context = ssl.create_default_context()
    if 'hotmail' in conf['email']:
        smtp = smtplib.SMTP('SMTP.office365.com', 587)
    else:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls(context=context)
    smtp.ehlo()
    smtp.login(conf['email'], conf['password'])
    smtp.send_message(msg)
    smtp.quit()
