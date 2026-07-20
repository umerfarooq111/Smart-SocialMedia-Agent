from pydantic import BaseModel

class ProductDetails(BaseModel):
    name: str
    price: float
    currency: str
    availability: str
    product_url: str
    description: str | None = None


class ProductSearchResponse(BaseModel):
    status: str
    product: ProductDetails | None = None
    message: str