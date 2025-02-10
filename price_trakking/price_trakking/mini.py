import requests as r
import bs4
from datetime import datetime
import time 
import schedule 

product_list = [
    {'id': 'B09V4FNFHN', 'name': 'Product 1'},
    {'id': 'B0C1GX5RVW', 'name': 'Product 2'},
    {'id': 'B0C9J97S7Q', 'name': 'Product 3'}
]

base_url ='https://www.amazon.in'
url = 'https://www.amazon.in/dp/'
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

base_response = r.get(base_url, headers=headers)
cookies = base_response.cookies

def track_prices():
    print(datetime.now())
    for prod in product_list:
        product_response = r.get(url+prod['id'], headers=headers, cookies=cookies)
        soup = bs4.BeautifulSoup(product_response.text, features='lxml')
        price_lines = soup.find(class_="a-price-whole")
        product_name = soup.find(id="productTitle").get_text().strip()  # Extracting product name
        
        if price_lines:
            final_price = price_lines.get_text().strip()
            print(f"{prod['name']}: {final_price}")
        else:
            print(f"Price not available for {prod['name']}")

schedule.every(5).seconds.do(track_prices)

while True:
    schedule.run_pending()
    time.sleep(1)
