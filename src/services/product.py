from src.model import Product
from redis_service import RedisService
import uuid


class ProductService:
    def __init__(self):
        pass

    def create_or_update_products(self, SESSION, records):
        caching_data = {}
        for record in records:
            product = SESSION.query(Product).filter_by(name=record["name"]).first()
            if product:
                # don't update if price hasn't changed
                if product.price == record["price"]:
                    continue
                # If the product exists, update it
                product.image = record["image"]
                product.price = record["price"]
                SESSION.add(product)
            else:
                # If the product doesn't exist, create a new one
                product = Product(
                    id=uuid.uuid4(),
                    name=record["name"],
                    image=record["image"],
                    price=record["price"],
                )
                SESSION.add(product)
            caching_data[str(product.id)] = {
                "name": product.name,
                "image": product.image,
                "price": product.price,
            }
        SESSION.commit()
        RedisService().bulk_insert(caching_data)
