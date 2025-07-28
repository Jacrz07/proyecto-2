
def get_inventary_with_catalog_pipeline() -> list:

    return [
        {"$addFields": {
            "id_catalog_obj": {"$toObjectId": "$id_catalog"}
        }},
        {"$lookup": {
            "from": "catalogs",
            "localField": "id_catalog_obj",
            "foreignField": "_id",
            "as": "catalog_info"
        }},
        {"$unwind": "$catalog_info"},
        {"$project": {
            "_id": 0,  
            "id": {"$toString": "$_id"},
            "id_catalog": {"$toString": "$id_catalog"},
            "name": "$catalog_info.name",
            "obtaining_date" : "$obtaining_date",
            "initial_quantity" : "$initial_quantity",
            "sold_quantity" : "$sold_quantity",
            "active": "$active"
        }},
    ]


