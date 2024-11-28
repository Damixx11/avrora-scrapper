import math
import requests
from bs4 import BeautifulSoup
import time
from colorama import Fore, Style

# URL y configuración
base_url = "https://avrora.ua/vsi-tovary/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}

# Hacer la solicitud
response = requests.get(base_url, headers=headers)
time.sleep(2)  # Añadir un retraso para evitar sobrecargar el servidor

if response.status_code == 200:
    content = response.text
    soup = BeautifulSoup(content, "html.parser")

    # Total de productos
    total_product_amount_text = soup.select_one("#search_total_items_st_update").get_text()
    total_product_amount = int(total_product_amount_text)
    print(Fore.YELLOW + f"Productos en total: {total_product_amount}" + Style.RESET_ALL)

    # Total de páginas (redondeo hacia arriba)
    product_per_page = 48
    total_product_pages = math.ceil(total_product_amount / product_per_page)
    print(Fore.YELLOW + f"Total de páginas: {total_product_pages}" + Style.RESET_ALL)

    # Recorrer cada página y extraer productos
    for page in range(1, total_product_pages + 1):
        print(Style.RESET_ALL + f"\n Page {page}/{total_product_pages}...")
        page_url = f"{base_url}?page={page}"
        response = requests.get(page_url, headers=headers)
        time.sleep(2)  # Pausa para no sobrecargar el servidor

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            page_content = response.text
            page_soup = BeautifulSoup(page_content, "html.parser")

            # Buscar todos los productos en la página
            products = page_soup.select('.ty-column4')

            # Procesar cada producto
            for product in products:
                bsProduct = BeautifulSoup(str(product), "html.parser")

                # Nombre del producto
                name = bsProduct.select_one('.product-title')
                name = name.get_text(strip=True) if name else "No disponible"

                # Categoría
                input_element = bsProduct.find("input", {"name": "restudio_gtm"})
                category = input_element.attrs.get("data-item-category", "No disponible") if input_element else "No disponible"

                # Imagen
                image = bsProduct.select_one('img')
                image_url = image['src'] if image else "No disponible"

                # ID del producto
                product_id_element = bsProduct.select_one('.ty-grid-list__item')
                product_id = product_id_element.attrs.get("data-product-id", "No disponible") if product_id_element else "No disponible"

                # Precio
                price = input_element.attrs.get('data-price', "No disponible") if input_element else "No disponible"

                # Descuento
                discount = input_element.attrs.get("data-discount", "No disponible") if input_element else "No disponible"

                # Imprimir la información
                print(Fore.CYAN + f"Nombre: {name}" + Style.RESET_ALL)
                print(f"Categoría: {category}")
                print(f"URL de la imagen: {image_url}")
                print(f"ID del producto: {product_id}")
                print(f"Precio: {price}")   
                print(f"Descuento: {discount}")
                print("--------------------")

else:
        print("Error al cargar la página, código de estado:", response.status_code)
