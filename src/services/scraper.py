import requests
from bs4 import BeautifulSoup
import urllib.parse
from src.services.product import ProductService
import time
import traceback

RETRY_DELAY = 5


class ScraperService:
    def __init__(self):
        pass

    def scrape_page(self, SESSION, page_limit=None, search_string=None):
        url_template = "https://dentalstall.com/shop/page/{page}/"
        if search_string:
            query_params = urllib.parse.urlencode({'s': search_string, 'post_type': 'product'})
            url_template += f"?{query_params}"
        page = 1
        total_products = 0
        while True:
            try:

                products = []
                url = url_template.format(page=page)
                print(url)
                # Send an HTTP GET request to the URL
                response = requests.get(url)
                # Check for server errors (status codes 500-599)
                if response.status_code >= 500 and response.status_code < 600:
                    print(
                        f"Server error ({response.status_code}). Retrying in {RETRY_DELAY} seconds..."
                    )
                    time.sleep(RETRY_DELAY)
                    continue  # Retry the request

                # Parse the HTML content of the webpage
                soup = BeautifulSoup(response.text, "html.parser")
                if soup.find("section", "error-404"):
                    print("No more products found")
                    break
                shop_content = soup.find("div", "mf-shop-content")
                all_items = shop_content.ul.find_all("li")
                for item in all_items:
                    try:
                        product_title, product_price, product_image = self.get_details(
                            item
                        )
                        if product_title and product_price and product_image:
                            products.append(
                                {
                                    "name": product_title,
                                    "image": product_image,
                                    "price": float(product_price),
                                }
                            )
                    except Exception as e:
                        traceback.print_exc()
                        continue

                total_products += len(products)
                ProductService().create_or_update_products(SESSION, products)
                print(f"Page {page} scrapped and updated in DB")
                page += 1
                if page_limit and page > page_limit:
                    break
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)  # Retry after a delay

            except Exception as e:
                traceback.print_exc()

                raise e

        return total_products

    def get_details(self, item):
        product_title = item.find("h2", "woo-loop-product__title")
        product_title = product_title.text if product_title else ""
        price_text = item.find("span", "woocommerce-Price-amount")
        price_text=price_text.get_text(strip=True) if price_text else ""
        product_price = "".join(filter(str.isdigit, price_text))
        product_image = (
            item.find("div", "mf-product-thumbnail")
            .find("a")
            .find("img")
        )
        product_image = product_image["src"] if "src" in product_image.attrs else ""
        return product_title, product_price, product_image
