# mail_sender.py
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')


def send_mail(email, subject, text):
    # if os.path.exists(dotenv_path):
    #     load_dotenv(dotenv_path)
    load_dotenv('.env')  # можно так
    addr_from = os.getenv('FROM')
    password = os.getenv('PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = email
    msg['Subject'] = subject
    body = text
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP_SSL(os.getenv('HOST'),
                              int(os.getenv('PORT')))
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
    return True

# send_mail('lux-nova@mail.ru', 'test', 'test')

# виджет с картой можно взять прямо с Яндекс-карты!

# ещё пару слов о системном администрировании: Paramico
#