import sqlite3
import requests
from bs4 import BeautifulSoup
from termcolor import colored

base_url = "https://scrapeme.live/shop/page/"

# Tüm sayfalardaki ürünleri toplamak için boş bir liste oluşturur
all_products = []

# Sayfaları dolaşma
for page_num in range(1, 49): 
    url = base_url + str(page_num) + "/"
    response = requests.get(url)
    page_content = response.text
    soup = BeautifulSoup(page_content, "html.parser")

    product_elements = soup.find_all("li", class_="product")

    for product_element in product_elements:
        name = product_element.find("h2", class_="woocommerce-loop-product__title").text.strip()
        price = product_element.find("span", class_="woocommerce-Price-amount").text.strip()

        # Ürünün sayfasına yönlendirme
        product_url = product_element.find("a")["href"]
        product_response = requests.get(product_url)
        product_page_content = product_response.text
        product_soup = BeautifulSoup(product_page_content, "html.parser")

        # Description ve stock bilgilerini çekme
        description_element = product_soup.find("div", class_="woocommerce-Tabs-panel--description")
        description = description_element.find("p").get_text(strip=True) if description_element and description_element.find("p") else ""

        stock_element = product_soup.find("p", class_="stock")
        stock = stock_element.get_text(strip=True) if stock_element else ""

        product = {
            "name": name,
            "price": price,
            "description": description,
            "stock": stock
        }

        all_products.append(product)

# SQLite veritabanı bağlantısı kurma
conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# Tabloyu oluşturma
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price TEXT,
        description TEXT,
        stock TEXT
    )
''')

# Verileri tabloya ekleme
for product in all_products:
    name = product["name"]
    price = product["price"]
    description = product["description"]
    stock = product["stock"]

    cursor.execute("INSERT INTO Products (name, price, description, stock) VALUES (?, ?, ?, ?)", (name, price, description, stock))

# Değişiklikleri kaydetme
conn.commit()

# Verileri görüntüleme
cursor.execute("SELECT * FROM Products")
rows = cursor.fetchall()

# Tablo başlıklarını görüntüleme
columns = [description[0] for description in cursor.description]
print("{:<5} {:<15} {:<10} {:<30} {:<10}".format(*columns))

# Verileri yeşil renkte görüntüleme
for row in rows:
    formatted_row = list(row)
    stock_index = columns.index("stock")
    formatted_row[stock_index] = colored(formatted_row[stock_index], "green")
    print("{:<5} {:<15} {:<10} {:<30} {:<10}".format(*formatted_row))

# Veritabanı bağlantısını kapatma
conn.close()
