from fastapi import APIRouter

from product_inventory.rest.api.v1 import healthcheck, products


v1 = APIRouter()

v1.include_router(healthcheck.router, tags=["healthcheck"])
v1.include_router(products.router, tags=["products"])