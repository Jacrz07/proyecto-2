from pydantic import BaseModel, Field, model_validator
from typing import Optional
from datetime import datetime

class Inventary(BaseModel):

    id: Optional[str] = Field(
        default = None,
        description= "ID de MongoDB, no se debe enviar en el POST"
    )

    id_catalog : str = Field(
        description= "ID del catalog de juego",
        examples= ["07f1f77bcf86cd799439"]
    )

    obtaining_date : datetime = Field(
        description= "fecha de adquisión del lote del juego",
        default_factory= datetime.utcnow
    )

    initial_quantity : int = Field(
        description= "cantidad de unidades inicial en el lote",
        gt= 0,
        examples= [50, 100]
    )

    sold_quantity : int = Field(
        description= "cantidad vendida del lote",
        ge= 0
    )

    active : bool = Field(
        description= "estado activo del lote",
        default= True
    )

    @model_validator(mode="after")
    def validate_sold_quantity(self):
        if self.sold_quantity > self.initial_quantity:
            raise ValueError("la cantidad vendida no puede ser mayor a la cantidad inicial")
        return self
