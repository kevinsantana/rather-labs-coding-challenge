from pydantic import BaseModel, Field


class Pagination(BaseModel):
    next: str = Field(..., description="Next result page")
    previous: str = Field(..., description="Previous result page")
    first: str = Field(..., description="First result page")
    last: str = Field(..., description="Last result page")
    total: int = Field(..., description="Total pages")
