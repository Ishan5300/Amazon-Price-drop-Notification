import requests
from glob import glob
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
prod_df=pd.read_csv(r"G:\Projects Python\Amazon Scrapper\itemlist.csv",encoding='utf-8')
prod_urls=prod_df.URLs
expected_price=prod_df.threshold
prod_name=prod_df.Code
def check_price():
    list_url=[]
    list_item=[]
    for i in range(0,len(prod_urls)):
        page=requests.get(prod_urls[i],headers=HEADERS)
        soup = BeautifulSoup(page.content, features="lxml")
        title=soup.find(id="productTitle").get_text().strip()
        #print(title)
        availability=soup.find(id="availability").get_text().strip()
        #print(availability)
        if(availability.count("Currently unavailable.")==0):
            try:
                price=soup.find(id="priceblock_ourprice").get_text().replace('₹','').replace(',','').strip()
                price=float(price)
            except:
                price=0
        #print(expected_price[i])
        #print(price)
            if((price!=0) and (price<expected_price[i])):
                list_item.append(prod_name[i])
                list_url.append(prod_urls[i])
               
        sleep(5)
    send_mail(list_url,list_item)
def send_mail(item_url,item_name):
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('sendermail@gmail.com','password')
    message = MIMEMultipart("alternative")
    message["Subject"]="Price is Down"
    message["Body"]='Check the link'
    message["FROM"]="sendermail@gmail.com"
    message["TO"]="receivermail@gmail.com"
    text="""\
    Check out these links
    """

    html="""\
    <! DOCTYPE html>
    <title>
    </title>
    <p>Following are the links</p>
    <table style="width:100%">
        {somelist}
        <tr>{somelistu}</tr>
    </table>
    <p>Thank you.</p>
    </html>
    """.format(
    somelist='\n'.join(["<td>" +item for item in item_name]),
    somelistu='\n'.join(["<td>" +item for item in item_url]))
    part1=MIMEText(text, "plain")
    part2=MIMEText(html,"html")
    message.attach(part1)
    message.attach(part2)
    try:
        server.sendmail(
        'sendermail@gmail.com',
        'receivermail@gmail',
        message.as_string()
        )
        print("mail sent")
    except:
        print("ERROR")
    finally:
        server.quit()
def print_msg(item_url,item_name):
    for i in range(0,len(item_url)):
        print(item_url[i])
        print(item_name[i])
check_price()
