import requests
from bs4 import BeautifulSoup
import time
from db_client import DBClient
from colorama import Fore, Style
# URL y configuración
url = "https://avrora.ua/vsi-tovary/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

# Hacer la solicitud
response = requests.get(url, headers=headers)

# Añadir un retraso si haces múltiples solicitudes
time.sleep(2)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    content = response.text
    # Parsear con BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")
    total_product_amount = soup.select_one("#search_total_items_st_update").get_text()
    total_product_amount = int(total_product_amount)
    print(Fore.YELLOW + f"products in total: {total_product_amount}" + Style.RESET_ALL)
    product_per_page = 48
    total_product_pages = total_product_amount / product_per_page
    print(Fore.YELLOW + f"total pages: {int(total_product_pages)}" + Style.RESET_ALL)




    # Buscar todos los productos dentro de los div con clase "ty-column4" vamos que es lo mismo y pues eso
    products = soup.select('.ty-column4')

    # Recorrer cada producto para extraer la información deseada
    for product in products:
        # Parsear cada producto individualmente
        bsProduct = BeautifulSoup(str(product), "html.parser")

        input_element  = bsProduct.find("input", {"name": "restudio_gtm"})
        print(input_element.attrs)

       ###############################################################
        #  nombre
        name = bsProduct.select_one('.product-title')  # Cambia 'product-title-class' por la clase real del nombre
        name = name.get_text(strip=True) if name else "No disponible"

        #  categoria
        category = input_element.attrs["data-item-category"]

        #  imagen
        image = bsProduct.select_one('img')
        image_url = image['src'] if image else "No disponible"

        # ID producto
        product_id = bsProduct.select_one('.ty-grid-list__item').attrs["data-product-id"]

        #  precio
        price = input_element.attrs['data-price']

        # descuento
        discount = input_element.attrs["data-discount"]
       ###############################################################

        # Imprimir la información
        print(f"Name: {name}")
        print(f"Type: {category}")
        print(f"Image URL: {image_url}")
        print(f"ID: {product_id}")
        print(f"Price: {price}")
        print(f"Discount: {discount}")
        print("--------------------")
        db_client = DBClient('postgresql://postgres:111@localhost/scrapper')
        db_client.add_product(name, price, discount, product_id, image.attrs["src"], category)


else:
    print("Failed to fetch the page, status code:", response.status_code)

