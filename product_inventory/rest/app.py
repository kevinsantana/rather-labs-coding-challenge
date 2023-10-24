import urllib3
from datetime import datetime

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from product_inventory.rest.routes import v1
from product_inventory.version import __version__
from product_inventory.exceptions import BaseException


urllib3.disable_warnings()

def include_router(app: FastAPI):
    app.include_router(v1, prefix="/v1")


def load_exceptions(app: FastAPI):
    @app.exception_handler(BaseException)
    async def base_exception_handler(
        request: Request, exception: BaseException
    ):  # pragma: no cover
        return JSONResponse(
            status_code=exception.status,
            content={
                "timestamp": str(datetime.now()),
                "status": exception.status,
                "error": exception.error,
                "message": exception.message,
                "method": request.method,
                "path": request.url.path,
                "error_details": exception.error_details,
            },
        )


def start_application():
    app = FastAPI(
        title="PRODUCT-INVENTORY-API",
        version=__version__,
        docs_url="/v1/docs",
    )
    include_router(app)
    load_exceptions(app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_credentials=True,
        allow_headers=["*"],
    )
    return app
