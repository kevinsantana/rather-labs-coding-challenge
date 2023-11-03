from product_inventory.database import DataBase
from product_inventory.models.product import ProductCategory


class Product(DataBase):
    def __init__(
        self,
        id: int = None,
        name: str = None,
        description: str = None,
        price: float = None,
        quantity: int = None,
        category: ProductCategory = None,
    ):
        self.__name = name
        self.__description = description
        self.__price = price
        self.__quantity = quantity
        self.__category = category

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def price(self):
        return self.__price

    @property
    def quantity(self):
        return self.__quantity

    @property
    def category(self):
        return self.__category

    def dict(self):
        return {
            key.replace("_Product__", ""): value
            for key, value in self.__dict__.items()
            if value
        }

    def search_by_query(
        self, limit: int, offset: int, min_price: float = None, max_price: float = None
    ):
        if offset:
            self.__offset = (offset - 1) * limit if offset != 1 else 1
        if limit:
            self.__limit = limit
        if min_price:
            self.__min_price = min_price
        if max_price:
            self.__max_price = max_price

        self.query_string = """SELECT * FROM public.product"""

        if any([self.__name, self.description, min_price, max_price, self.__category]):
            self.query_string += " WHERE"

        if self.__name:
            self.query_string += " name = %(name)s"

        if min_price and max_price:
            self.query_string += " AND PRICE BETWEEN %(min_price)s AND %(max_price)s"

        elif min_price and not max_price:
            self.query_string += " AND PRICE < %(min_price)s"

        elif max_price and not min_price:
            self.query_string += " AND PRICE > %(max_price)s"

        if self.__category:
            self.query_string += " AND category = %(category)s"

        if offset and limit:
            self.query_string += " LIMIT %(limit)s OFFSET %(offset)s"
        elif offset and not limit:
            self.query_string += " OFFSET %(offset)s"
        elif limit and not offset:
            self.query_string += " LIMIT %(limit)s"

        products, total = self.find_all(total=True)
        return total, [Product(**dict(product)) for product in products]
