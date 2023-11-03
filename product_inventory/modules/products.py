from product_inventory.database.product import Product

from product_inventory.models.product import ProductCategory


def search(
    name: str = None,
    min_price: float = None,
    max_price: float = None,
    category: ProductCategory = None,
    offset: int = None,
    limit: int = None,
):
    total, products = Product(
        name=name,
        category=category,
    ).search_by_query(limit, offset, min_price, max_price)
    return total, [product.dict() for product in products]
