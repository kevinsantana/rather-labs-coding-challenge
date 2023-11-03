from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from product_inventory.models.pagination import Pagination


class ProductCategory(str, Enum):
    eletronics: str = "Eletronics"
    clothing: str = "Clothing"
    food: str = "Food"


class Product(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    category: ProductCategory
