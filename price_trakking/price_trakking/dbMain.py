import requests
from bs4 import BeautifulSoup
import smtplib
import sqlite3
from datetime import datetime

# URL = "https://www.amazon.com/Xiaomi-X6-Unlocked-Tmobile-Charger/dp/B0CPXX34K2/ref=sr_1_3?dib=eyJ2IjoiMSJ9.sinx92ntFmdgWVkcRlXzk17FFwkjcBGHH3BAU9G0svkTELi4ojKkEK7RU7oaZqCH8pxAERf8YpuJCyCeQahUea2sICF0ZGKL4VRLNEZxSr4FYqTEJ6LJglMK72QwybPnt35zsr-W-63SPMCDbE41NOjT_U5kebWpdnvw8-ap74GVdUEvhj3QoXh8X2UX9HAOpGHLoAeKsLtObcFJa-mG5sWu-4PQIGgseOlm_0v76XY.hDVP4fqK6cUtJVicY-w6hQhJMmaJzrkdD4LExlpdqdA&dib_tag=se&keywords=poco%2BX6&sr=8-3&th=1"
URL = "https://www.amazon.com/Xiaomi-Camera-Factory-Unlocked-Smartphone/dp/B08B3QSVM6/ref=slsr_d_dpds_fsdp4star_fa_xcat_cheapdynam_d_sccl_2_1/137-0094325-4523156?pd_rd_w=l8Qia&content-id=amzn1.sym.97982461-5444-416f-a4ee-edf7adedb7ec&pf_rd_p=97982461-5444-416f-a4ee-edf7adedb7ec&pf_rd_r=D68KR2NYAWFNC4BR9CMZ&pd_rd_wg=ngFVF&pd_rd_r=db463acd-168c-40e3-a55e-586de1b26193&pd_rd_i=B08B3QSVM6&psc=1"

'''headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}'''

# Connect to SQLite database
conn = sqlite3.connect('prices.db')
c = conn.cursor()

# Create table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS prices
             (timestamp TEXT, title TEXT, price FLOAT)''')
conn.commit()

response = requests.get(URL)
#response = requests.get(URL, headers=headers)
#print(response.content)

with open('file.txt', 'w') as file:
    file.write(str(response.content))

soup = BeautifulSoup(response.content, "lxml")
price = soup.find(class_="a-offscreen").get_text()
print(price)

price_as_list = list(price)
price_as_list.pop(0)
res = []
for char in price_as_list:
    if char != ',':
        res.append(char)
price_as_string = "".join(res)
price_as_float = float(price_as_string)

print(price_as_float)

title = soup.find(id="productTitle").get_text().strip()
print(title)

BUY_PRICE = 140

# Insert data into the database
c.execute("INSERT INTO prices (timestamp, title, price) VALUES (?, ?, ?)", (datetime.now(), title, price_as_float))
conn.commit()

if price_as_float < BUY_PRICE:
    # send an email alert
    message = f"{title} is now available in {price}"

    recipients = ['cs21b1003@iiitr.ac.in', 'abhaysuresh0810@gmail.com', 'cs20b1018@iiitr.ac.in','cs21b1039@iiitr.ac.in']  # Add your recipient email addresses here

    
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        result = connection.login('ashutoshshukla4599@gmail.com', 'merh htwo gwen reiz')
        print(result)
        connection.sendmail(
            from_addr='ashutoshshukla4599@gmail.com',
            to_addrs= recipients,
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode("utf-8")
        )

# Close the database connection
conn.close()
