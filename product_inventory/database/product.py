from product_inventory.database import DataBase
from product_inventory.models.product import ProductCategory


class Product(DataBase):
    def __init__(
        self,
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
