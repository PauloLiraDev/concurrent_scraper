from pydantic import BaseModel

class Product(BaseModel):
    id: str
    name: str
    category: str
    price: str
    stock: str