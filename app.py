#!/usr/bin/env python

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP_SSL, SMTPException, SMTPAuthenticationError

import requests
from bs4 import BeautifulSoup

CODING = 'utf-8'

GRI_BASE_URL = 'http://www.gri-formationprofessionnelle.ch/'
GRI_LOGIN_URL = GRI_BASE_URL + 'index.php?page=CheckLogin'
GRI_HOME = GRI_BASE_URL + 'index.php?page=163A456F_493PID000Af0851945244340'

GMAIL_LOGIN = ''
GMAIL_PASSWORD = ''

GRI_LOGIN = ''
GRI_PASSWORD = ''


def main():
    s = requests.session()
    login_data = dict(username=GRI_LOGIN, password=GRI_PASSWORD, submit='Login')
    s.post(GRI_LOGIN_URL, data=login_data)
    r = s.get(GRI_HOME)
    soup = BeautifulSoup(r.text, 'html.parser')
    note = soup.find_all("div", class_="txtTITRE")[0].text

    if len(note) > 0:
        outer_msg = message(note)
        outer_msg[0].attach(outer_msg[1])
        try:
            gmail(outer_msg[0])
        except (SMTPException, SMTPAuthenticationError) as error:
            print(error)


def gmail(mail):
    server = SMTP_SSL('smtp.gmail.com', 465, timeout=10)
    server.login(GMAIL_LOGIN, GMAIL_PASSWORD)
    server.sendmail(GMAIL_LOGIN, GMAIL_LOGIN, mail.as_string())


def message(note):
    outer = MIMEMultipart()
    outer['Subject'] = Header('Note reçue : ' + note, CODING)
    msg = MIMEText('', 'plain', CODING)

    return outer, msg

if __name__ == '__main__':
    main()
