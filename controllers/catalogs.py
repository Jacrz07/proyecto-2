from models.catalogs import Catalog
from utils.mongodb import get_collection
from pipelines.catalog_pipelines import get_catalog_sales_pipeline, get_discount_catalogs_pipeline
from fastapi import HTTPException
from bson import ObjectId

coll = get_collection("catalogs")
coll_inventary = get_collection("inventary")

async def get_catalogs() -> list[Catalog]:

    try:
        catalogs = []
        for doc in coll.find():
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            catalog = Catalog(**doc)
            catalogs.append(catalog)    
        return catalogs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching catalogs: {str(e)}")


async def get_catalog_by_id(catalog_id : str) -> Catalog:

    try:
        catalog = coll.find_one({"_id" : ObjectId(catalog_id)})
        if not catalog:
            raise  HTTPException(status_code=404, detail="Catalog not found")

        catalog["id"] = str(catalog["_id"])
        del catalog["_id"]
        return Catalog(**catalog)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching catalog: {str(e)}")
    

async def create_catalog(catalog : Catalog) -> Catalog:

    try:
        catalog.name = catalog.name.strip()
        catalog.description = catalog.description.strip()
        catalog.plataform = catalog.plataform.strip()

        existing_catalog = coll.find_one({"name": {"$regex": f"^{catalog.name}$", "$options": "i"}})
        if existing_catalog:
            raise HTTPException(status_code=400, detail="Catalog with this name already exists")
    
        catalog_dict = catalog.model_dump(exclude={"id"})
        inserted = coll.insert_one(catalog_dict)
        catalog.id = str(inserted.inserted_id)

        return catalog
    
    except HTTPException: 
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating catalog: {str(e)}")
    
    
async def update_catalog(catalog_id: str, catalog: Catalog) -> Catalog:
    
    try:
        catalog.name = catalog.name.strip()
        catalog.description = catalog.description.strip()
        catalog.plataform = catalog.plataform.strip()

        catalog_ = coll.find_one({"_id" : ObjectId(catalog_id)})
        catalog_["id"] = str(catalog_["_id"])
        del catalog_["_id"]

        if Catalog(**catalog_).name != catalog.name:
            raise HTTPException(status_code=400, detail="Catalog name can not be changed")
        
        result = coll.update_one(
            {"_id": ObjectId(catalog_id)},
            {"$set": catalog.model_dump(exclude={"id"})}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Catalog to update not found or not changes introduced")

        return await get_catalog_by_id(catalog_id)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating catalog: {str(e)}")
    
    
async def get_catalog_sales() -> list:
    try:
        pipeline = get_catalog_sales_pipeline()
        result = list(coll_inventary.aggregate(pipeline))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching catalog with sales: {str(e)}")
    

async def get_catalog_by_filter(
    name: str,  
    plataform: str,
    max_price: float, 
    limit: int = 10, 
    skip: int = 0) -> list[Catalog]:

    try:
        query = {}
        if name:
            query["name"] = { "$regex": name, "$options": "i" }
        if plataform:
            query["plataform"] = { "$regex": plataform, "$options": "i" }
        if max_price:
            query["cost"] = {"$lte" : max_price}

        results = coll.find(query).skip(skip).limit(limit)
        catalogs = []
        for doc in results:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            catalog = Catalog(**doc)
            catalogs.append(catalog)
        return catalogs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
async def get_discount_catalogs() -> list:
    try:
        pipeline = get_discount_catalogs_pipeline()
        result = list(coll.aggregate(pipeline))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching discount catalogs: {str(e)}")


async def deactivate_catalog(catalog_id: str) -> Catalog:

    try:
        result = coll.update_one(
            {"_id": ObjectId(catalog_id)},
            {"$set": {"active": False}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Catalog not found")

        return await get_catalog_by_id(catalog_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deactivating catalog: {str(e)}")
