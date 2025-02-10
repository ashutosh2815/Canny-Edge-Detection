import streamlit as st
import requests
from bs4 import BeautifulSoup
import smtplib
import sqlite3
from datetime import datetime

def track_amazon_price(url, buy_price, recipients):
    conn = sqlite3.connect('prices.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS prices
                 (timestamp TEXT, title TEXT, price FLOAT)''')
    conn.commit()

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    price = soup.find(class_="a-offscreen").get_text()

    price_as_list = list(price)
    price_as_list.pop(0)
    res = []
    for char in price_as_list:
        if char != ',':
            res.append(char)
    price_as_string = "".join(res)
    price_as_float = float(price_as_string)

    title = soup.find(id="productTitle").get_text().strip()

    c.execute("INSERT INTO prices (timestamp, title, price) VALUES (?, ?, ?)", (datetime.now(), title, price_as_float))
    conn.commit()

    if price_as_float < buy_price:
        message = f"{title} is now available for {price}"
        with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
            connection.starttls()
            result = connection.login('your_email@gmail.com', 'your_password')
            connection.sendmail(
                from_addr='your_email@gmail.com',
                to_addrs=recipients,
                msg=f"Subject:Amazon Price Alert!\n\n{message}\n{url}".encode("utf-8")
            )

    conn.close()

def main():
    st.title("Amazon Price Tracker")

    url = st.text_input("Enter Amazon Product URL:")
    buy_price = st.number_input("Enter Buy Price:")
    recipients = st.text_area("Enter Recipients (separated by comma):")

    if st.button("Track Price"):
        recipients_list = recipients.split(',')
        track_amazon_price(url, buy_price, recipients_list)
        st.success("Price tracking started!")

if __name__ == "__main__":
    main()
