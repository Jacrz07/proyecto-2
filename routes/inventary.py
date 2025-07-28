from fastapi import APIRouter, Request
from models.inventary import Inventary
from controllers.inventary import (
    create_inventary, 
    get_inventary_with_catalog_details,
    get_inventary_by_id,
    update_inventary,
    get_all_inventary_from_catalog,
    deactivate_inventary,
)
from utils.security import validateadmin

router = APIRouter()

@router.post("/inventary", response_model=Inventary, tags= ["Inventary"])
@validateadmin
async def create_inventary_endpoint(request: Request, inventary: Inventary) -> Inventary:
    return await create_inventary(inventary)


@router.get("/inventary", response_model= list, tags=["Inventary"])
@validateadmin
async def get_inventary_endpoint(request:Request) -> list:
    return await get_inventary_with_catalog_details()


@router.get("/inventary/{inventary_id}", tags=["Inventary"])
@validateadmin
async def get_inventary_with_id_endpoint(request: Request, inventary_id: str):
    return await get_inventary_by_id(inventary_id)


@router.put("/inventary/{inventary_id}", tags=["Inventary"])
@validateadmin
async def get_inventary_with_id_endpoint(request: Request, inventary_id: str, inventary: Inventary):
    return await update_inventary(inventary_id, inventary)


@router.get("/inventary/catalogs/{id_catalog}", response_model= list[Inventary], tags=["Inventary"])
@validateadmin
async def get_inventary_with_id_endpoint(request: Request, id_catalog: str) -> list[Inventary]:
    return await get_all_inventary_from_catalog(id_catalog)


@router.delete("/inventary/{inventary_id}", response_model= Inventary, tags= ["Inventary"])
@validateadmin
async def deactivate_inventary_endpoint(request: Request, inventary_id: str) -> Inventary:
    return await deactivate_inventary(inventary_id)