from enum import Enum


class ProductCategory(str, Enum):
    eletronics: str = "Eletronics"
    clothing: str = "Clothing"
    food: str = "Food"
