from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Order(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Se genera automáticamente desde el _id de MongoDB"
    )

    id_user: str = Field(
        description="ID del usuario que realizó la orden",
        examples=["507f1f77bcf86cd799439011"]
    )

    date: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha de creación de la orden"
    )

    total: float = Field(
        description="Total de la orden",
        gt=0,
        examples=[165.55, 109.98]
    )

    adress: str = Field(
        description="dirección de envío de la orden",
        examples= "colonia juan, casa tal"
    )

    