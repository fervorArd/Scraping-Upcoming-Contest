import requests
import datetime
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formatdate

statusOK = u"Found / "
statusNG = u"Not Found"

# Make http request
response = requests.get('https://www.hackerearth.com/challenges/')
time.sleep(5)

# Check response
for url in ['https://www.hackerearth.com/challenges/']:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'Http error has occurred: {http_err}')
    except Exception as err:
        print(f'Other error has occurred: {err}')
    else:
        print("Success!")


# Scrape the data from the website
scrape = ''
html = response.text
soup = BeautifulSoup(html, 'html.parser')
parent = soup.find("div", {"class": "upcoming challenge-list"})
divtag = parent.find_all("div", {"class": "challenge-card-modern"})

for tag in divtag:
    target = tag.find_all("a", {"class": "challenge-card-wrapper challenge-card-link"})
    for link in target:
        name = link.get('href')
        prefix = 'https://www.hackerearth.com'
        if name[:27] != prefix:
            name = prefix + name
            print("REGISTRATION LINK : ", name)
            scrape += "REGISTRATION LINK :\n" + name + '\n\n'
        else:
            print("REGISTRATION LINK : ", name)
            scrape += "REGISTRATION LINK :\n" + name + '\n'

    challenge_name = tag.find("div", {"class": "challenge-name ellipsis dark"})
    print("CHALLENGE NAME : " + challenge_name.getText())
    scrape += "CHALLENGE NAME :\n" + challenge_name.getText() + '\n'

    starts_on = tag.find("div", {"class": "date less-margin dark"})
    print("STARTS ON : " + starts_on.getText())
    scrape += "STARTS ON :\n" + starts_on.getText() + '\n\n\n'

    print()


# Sending scraped data from website to gmail

web_charset = "utf-8"
mail_charset = "ISO-2022-JP"

from_address = "scrape2email@gmail.com"
from_password = "testing@!21"
to_address = "reciever'semailaddr"

def createmsg(from_addr, to_addr, subject, body, encoding):
    # Create text message
    msg = MIMEText(body, 'plain', encoding)
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = Header(subject, encoding)
    msg['Date'] = formatdate(localtime=True)
    return msg


def sendmail(subject, body):
    # Get the msg
    msg = createmsg(from_address, to_address, subject, body, mail_charset)

    # Set up connection to the gmail mail server
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)

    # Identify yourself to an ESMTP server using ehlo
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()

    # Login to the gmail account
    mailserver.login(from_address, from_password)

    # Send the email message
    mailserver.sendmail(from_address, to_address, msg.as_string())

    mailserver.quit()


if __name__ == "__main__":
    date = datetime.datetime.today()
    time = date.strftime("%Y-%m-%d %H-%M-%S")
    mailsubject = u"Upcoming Hackerearth Contest" + time
    mailbody = scrape
    sendmail(mailsubject, mailbody)
