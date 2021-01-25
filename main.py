import lxml
from bs4 import BeautifulSoup
import requests
from smtplib import SMTP
from email.mime.text import MIMEText
import json


print('Welcome to Amazon Wishlist Price Tracker')
print('----------------------------')
print('Please be sure that every item has a price in your wishlist.')
print('------------------------------------')

MAIL = YOUR EMAIL
PASSWRD = YOUR EMAIL PSSWD
# + OBJECT ID!!!!!
sheety_end = SHEETY ENDPOINT
sheety_usr = YOUR API CREDENTIAL
sheety_psw = YOUR API CREDENTIAL
amazon_wishlist_url = AMAZON WISHLIST URL (NEEDS TO BE PUBLIC)
def send_mail(topic, body):
    text_type = 'plain'
    text=body
    recipients = [YOUR RECIPIENTS]
    msg = MIMEText(text, text_type, 'utf-8')
    msg['Subject'] = topic
    msg['To'] = ', '.join(recipients)
    msg['From'] = YOUR EMAIL ACCOUNT
    with SMTP(host='smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(MAIL, PASSWRD)
        connection.sendmail(MAIL, recipients, msg.as_string())

def update_sheets(data, i):
        data_ = {
            'wishlist': {
                'productName': data['title'],
                'newPrice': data['new_price'],
                'oldPrice': data['old_price'],
                'percentage': data['percentage']
            }
        }
        url = f'{sheety_end}{i+2}'
        response = requests.put(url, json=data_, auth=(sheety_usr, sheety_psw))
        print(response.text)


headers = {
    'User-Agent': YOUR USER AGENT 
}

threshold_percentage = 2#float(input('Please enter the minimum change percentage in order to be notified:\n'))
response = requests.get(amazon_wishlist_url, headers=headers)
#print(response.content)

soup = BeautifulSoup(response.content, 'lxml')
product_prices = [float(price.getText()[1: len(price.getText()) + 1]) for price in soup.select('span.a-offscreen')]  # this doesn't get every item in wishlist!
product_titles = [name_title.get('alt') for name_title in soup.select('div.a-text-center.g-itemImage img')]


with open('product_info.json', 'r') as pinfo:
    try:
        resp_json = json.load(pinfo)  # ACTUAL VALUES!!!
    except json.JSONDecodeError:
        pass
mail_body = ''
counter = 0

ppost_data = {
    'products': []
}
for i in range(0, len(product_prices)):
    try:
        new_price = resp_json['products'][i]['price']
    except (NameError, KeyError, IndexError):
        new_price = product_prices[i]
    print(new_price)
    post_data = {
        'title':product_titles[i],    
        'old_price': product_prices[i],
        'new_price': new_price,
        'percentage': round(((product_prices[i] - new_price)/product_prices[i]) * 100, 3),
    }
    
        
    #update_sheets(post_data, i)

    if post_data['percentage'] >= threshold_percentage:
        mail_body += f"•{post_data['title']}'s price has been dropped by %{post_data['percentage']}!\n\n"
        counter += 1
    
    with open('product_info.json', 'w') as json_p:
        
        ppost_data['products'].append(post_data)
        json.dump(ppost_data, json_p)
    
    



if counter >=1:
    mail_body += f"\n\nSheets URL: SHEETS URL'
    send_mail(topic='Wishlist!', body=mail_body)
