from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class Catalog(BaseModel):

    id: Optional[str] = Field(
        default = None,
        description = "se genera en MongoDB, no se debe enviar en el POST"
    )

    name: str = Field(
        description="Nombre del juego",
        min_length=1,
        max_length=100,
        examples=["God of War", "Resident Evil"]
    )

    description: str = Field(
        description= "descripción detallada del juego",
        min_length=1,
        max_length=500,
        examples= ["juego de acción-aventura"]
    )

    plataform: str = Field(
        description= "plataformas en las que está disponible",
        min_length=1,
        max_length=500,
        examples = ["Play station 4", "Xbox"]
    )

    release_date: datetime = Field(
        description= "fecha de lanzamiento de juego",
    )

    cost: float = Field(
        description="Costo del juego",
        gt=0,
        examples=[150.50, 89.99]
    )

    discount: int = Field(
        description="Descuento en porcentaje (0-100)",
        ge=0,
        lt=100,
        default=0,
        examples=[10, 25, 0]
    )

    active: bool = Field(
        default=True,
        description="Estado activo del catálogo"
    )


