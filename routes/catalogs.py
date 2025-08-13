from fastapi import APIRouter, Request
from models.catalogs import Catalog
from controllers.catalogs import (
    get_catalogs,
    get_catalog_by_id,
    create_catalog,
    update_catalog,
    deactivate_catalog,
    get_catalog_sales,
    get_catalog_by_filter,
    get_discount_catalogs
)
from utils.security import validateadmin
from utils.mongodb import get_collection

coll = get_collection("catalogs")

router = APIRouter()

@router.post("/catalogs", response_model=Catalog, tags= ["Catalogs"])
@validateadmin
async def create_catalog_endpoint(request: Request, catalog: Catalog) -> Catalog:
    return await create_catalog(catalog)


@router.get("/catalogs", response_model= list, tags=["Catalogs"])
async def get_catalogs_endpoint() -> list:
    return await get_catalogs()


@router.get("/catalogs/{catalog_id}", response_model=Catalog, tags=["Catalogs"])
async def get_catalog_by_id_endpoint(catalog_id: str) -> Catalog:
    return await get_catalog_by_id(catalog_id)


@router.put("/catalogs/{catalog_id}", response_model= Catalog, tags=["Catalogs"])
@validateadmin
async def update_catalog_endpoint(request: Request, catalog_id: str, catalog: Catalog) -> Catalog:
    return await update_catalog(catalog_id, catalog)


@router.get("/sales/catalogs", response_model= list, tags=["Catalogs"])
@validateadmin
async def get_catalogs_sales_endpoint(request: Request) -> list:
    return await get_catalog_sales()


@router.get("/filter/catalogs", response_model= list, tags=["Catalogs"])
async def get_catalog_by_filter_endpoint(request: Request, name: str = None,
    plataform : str = None,
    max_price: float = None,
    limit: int = 10,
    skip: int = 0 ) -> list:
    return await get_catalog_by_filter(name, plataform, max_price, limit, skip)


@router.get("/discount/catalogs", response_model= list, tags=["Catalogs"])
async def get_discount_catalogs_endpoint() -> list:
    return await get_discount_catalogs()



@router.delete("/catalogs/{catalog_id}", response_model= dict, tags=["Catalogs"])
@validateadmin
async def deactivate_catalog_endpoint(request: Request, catalog_id: str) -> dict:
    return await deactivate_catalog(catalog_id)

