import smtplib
from email.message import EmailMessage
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    msg = EmailMessage()
    msg['Subject'] = 'Hello'
    msg['From'] = 'andregaragon@gmail.com'
    msg['To'] = 'andregaragon@gmail.com'
    message_text = f"""
    <!DOCTYPE html>
    <html>
        <body>
            <p>Olá </p>

            <p>-Quantidade de Cotas:</p>

            <p>-Valor da cota: </p>

            <p>-Valor Financeiro Total:</p>

            <p>-Link do Prospecto:</p>
            <p>Aguardo a sua confirmação.</p>

            <p>Abraço</p>

            <b style="font-family:Calibri,Arial,Helvetica,sans-serif;line-height:16px; color:rgb(102,102,102);font-size:12px">Importante:</b>
            <p style="font-family:Calibri,Arial,Helvetica,sans-serif;line-height:16px; color:rgb(102,102,102);font-size:11px">
            A Manchester Agentes Autônomos de Investimentos S/S Ltda é uma empresa de agentes autônomos de investimento devidamente registrada na Comissão de Valores Mobiliários (CVM), na forma da Instrução Normativa nº 497/11. A Manchester Agentes Autônomos de Investimentos S/S Ltda. atua no mercado financeiro através da XP Investimentos CCTVM S/A, o que pode ser verificado através do site da CVM (<a href="https://www.gov.br/cvm/pt-br">www.cvm.gov.br</a> > Agentes Autônomos > Relação dos Agentes Autônomos contratados por uma Instituição Financeira > Corretoras > XP Investimentos) ou através do site da ANCORD para escritórios credenciados a partir de outubro de 2012 (<a href="http://www.ancord.org.br/Website_Ancord/index.html">http://www.ancord.org.br/Website_Ancord/index.html</a> > Agentes Autonomos > Consultas) ou através do site da própria XP Investimentos CCTVM S/A (<a href="https://www.xpi.com.br/">www.xpi.com.br</a> > Encontre um escritório > Selecione abaixo o estado e a cidade que deseja pesquisar > Veja a lista dos agentes autônomos). Na forma da legislação da CVM, o agente autônomo de investimento não pode administrar ou gerir o patrimônio de investidores. O agente autônomo é um intermediário e depende da autorização prévia do cliente para realizar operações no mercado financeiro. Esta mensagem, incluindo os seus anexos, contém informações confidenciais destinadas a indivíduo e propósito específicos, sendo protegida por lei. Caso você não seja a pessoa a quem foi dirigida a mensagem, deve apagá-la. É terminantemente proibida a utilização, acesso, cópia ou divulgação não autorizada das informações presentes nesta mensagem. As informações contidas nesta mensagem e em seus anexos são de responsabilidade de seu autor, não representando necessariamente ideias, opiniões, pensamentos ou qualquer forma de posicionamento por parte da Manchester Agentes Autônomos de Investimentos S/S Ltda. O investimento em ações é um investimento de risco e rentabilidade passada não é garantia de rentabilidade futura. Na realização de operações com derivativos existe a possibilidade de perdas superiores aos valores investidos, podendo resultar em significativas perdas patrimoniais. Para informações e dúvidas, favor contatar seu agente de investimentos. Para reclamações, favor contatar a Ouvidoria da XP Investimentos no telefone nº 0800-722-3710.
            </p>

        </body>
    </html>
    """

    smtp.login('andregaragon@gmail.com', 'A463112b*')
    smtp.send_message(msg)
