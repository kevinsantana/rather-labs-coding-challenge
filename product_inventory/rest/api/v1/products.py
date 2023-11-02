from typing import Annotated

from fastapi import APIRouter, Query, Request

from product_inventory.modules.products import search
from product_inventory.rest.api.v1 import make_pagination
from product_inventory.models.product import ProductCategory, Products

router = APIRouter()


@router.get(
    "/products", status_code=200, summary="Get products", response_model=Products
)
def products(
    request: Request,
    name: Annotated[str | None, Query(description="Product name")] = None,
    min_price: Annotated[float | None, Query(description="Min product price")] = None,
    max_price: Annotated[float | None, Query(description="Max product price")] = None,
    category: Annotated[
        ProductCategory | None, Query(description="Product category")
    ] = None,
    offset: Annotated[int | None, Query(description="Page to return", gt=0)] = None,
    qtd: Annotated[
        int | None, Query(description="Number of products to find", gt=0)
    ] = None,
):
    """
    Get products by given search query. If none, return all products.
    """
    total, products = search(name, min_price, max_price, category, offset, qtd)
    return make_pagination(products, qtd, offset, total, str(request.url))
