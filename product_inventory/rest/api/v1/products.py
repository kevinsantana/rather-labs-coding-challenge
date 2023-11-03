from typing import Annotated

from fastapi import APIRouter, Query, Request
from fastapi_pagination import LimitOffsetPage, paginate

from product_inventory.modules.products import search
from product_inventory.models.product import ProductCategory, Product

router = APIRouter()
from loguru import logger


@router.get(
    "/products",
    status_code=200,
    summary="Get products",
    response_model=LimitOffsetPage[Product],
)
def products(
    request: Request,
    name: Annotated[str | None, Query(description="Product name")] = None,
    min_price: Annotated[float | None, Query(description="Min product price")] = None,
    max_price: Annotated[float | None, Query(description="Max product price")] = None,
    category: Annotated[
        ProductCategory | None, Query(description="Product category")
    ] = None,
):
    """
    Get products by given search query. If none, return all products.
    """
    offset, limit = int(request.query_params.get("offset", 1)), int(
        request.query_params.get("limit", 50)
    )
    total, products = search(name, min_price, max_price, category, offset, limit)
    return paginate(products)
