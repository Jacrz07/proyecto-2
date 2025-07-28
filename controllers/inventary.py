from models.inventary import Inventary
from models.catalogs import Catalog
from pipelines.inventary_pipelines import get_inventary_with_catalog_pipeline
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

coll_inventary = get_collection("inventary")
coll_catalogs = get_collection("catalogs")

async def create_inventary(inventary : Inventary) -> Inventary:

    try:
        existing_catalog = coll_catalogs.find_one({"_id" : ObjectId(inventary.id_catalog)})
        catalog = Catalog(**existing_catalog)
        if catalog is None or not catalog.active:
            raise HTTPException(status_code=404, detail= "the catalog of the inventary does not exist or is inactive")
             
        inventary_dict = inventary.model_dump(exclude={"id"})
        inserted = coll_inventary.insert_one(inventary_dict)
        inventary.id = str(inserted.inserted_id)

        return inventary

    except HTTPException: 
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating inventary: {str(e)}")
       

async def get_inventary_with_catalog_details() -> list:

    try:
        pipeline = get_inventary_with_catalog_pipeline()
        inventary_list = list(coll_inventary.aggregate(pipeline))
        return inventary_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching inventary: {str(e)}")
    

async def get_inventary_by_id(inventary_id: str):
    try:
        inventary_list = await get_inventary_with_catalog_details()
        for doc in inventary_list:
            if doc["id"] == inventary_id:
                return doc
        raise HTTPException(status_code=404, detail="Inventary not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching inventary: {str(e)}")


async def update_inventary(inventary_id: str, inventary: Inventary):
    try:
        ex_inventary= coll_inventary.find_one({"_id" : ObjectId(inventary_id)})
        if not ex_inventary:
            raise HTTPException(status_code=400, detail="inventary not found")
        
        ex_inventary["id"] = str(ex_inventary["_id"])
        del ex_inventary["_id"]
        existing_inventary = Inventary(**ex_inventary)

        if existing_inventary.id_catalog != inventary.id_catalog:
            raise HTTPException(status_code=400, detail="id_catalog can not be changed")

        result = coll_inventary.update_one(
            {"_id": ObjectId(inventary_id)},
            {"$set": inventary.model_dump(exclude={"id", "id_catalog"})}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="inventary to update not found or not changes introduced")
        
        return await get_inventary_by_id(inventary_id)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating inventary: {str(e)}")


async def get_all_inventary_from_catalog(id_catalog : str) -> list[Inventary]:
    try: 
        inventary_from_catalog = []
        for doc in coll_inventary.find():
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            inventary = Inventary(**doc)
            if inventary.id_catalog == id_catalog:
                inventary_from_catalog.append(inventary)
        return inventary_from_catalog
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching inventary from catalogs: {str(e)}")


async def deactivate_inventary(id_inventary : str) -> Inventary:
    try:
        result = coll_inventary.update_one(
            {"_id": ObjectId(id_inventary)},
            {"$set": {"active": False}}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="inventary not found or already inactive")
        
        return await get_inventary_by_id(id_inventary)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deactivating inventary: {str(e)}")  

