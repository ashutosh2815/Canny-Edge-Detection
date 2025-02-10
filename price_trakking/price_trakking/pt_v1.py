import requests
from bs4 import BeautifulSoup
import time


l=[]
o={}


url="https://www.amazon.in/sspa/click?ie=UTF8&spc=MTo2OTMzNzAxMzcyNzEyMDMwOjE3MDY3MjYwNDc6c3BfYXRmOjMwMDEyNDg2MjExNzEzMjo6MDo6&url=%2FOnePlus-Silky-Black-RAM-512GB%2Fdp%2FB0CQPP73S8%2Fref%3Dsr_1_1_sspa%3Fcrid%3D1OP7C6VGMI4G9%26keywords%3Doneplus%26qid%3D1706726047%26sprefix%3Doneplus%252Caps%252C275%26sr%3D8-1-spons%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1"
headers={"accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3;q=0.7"}

resp = requests.get(url, headers=headers)
#print(resp.status_code)

soup=BeautifulSoup(resp.text,'html.parser')

#print(soup , "\n\n\n")

final_name= ""
final_price= ""
print(soup , "\n\n\n")

try:
    name = soup.find('span',{'id':'productTitle'})
    final_name = name.text.strip()
    
    o["title"]=final_name
except:
    o["title"]=None

try:
    price =soup.find("span",{"class":"a-price"}).find("span")
    final_price = price.text
    o["price"] = final_price
except:
    o["price"]=None
    

print(final_name)
print(final_price)

import csv

# Open the CSV file in "append" mode
with open("products.csv", "a", encoding="utf-8") as csvfile:
    # Create a CSV writer object
    writer = csv.writer(csvfile)
    #print(csvfile)
    print(o["title"])
    print(o["price"])
    # Write the extracted data as a new row
    if (o["title"] != None):
        writer.writerow([o["title"], o["price"]])
    print(o["title"])
    print(o["price"])

print("Title and price successfully appended")

