from bson import ObjectId

def get_catalogs_pipeline() -> list:
    return [
        {
            "$addFields": {
                "id": { "$toString": "$_id" }
            }
        },
        {
            "$lookup": {
                "from": "inventary",
                "localField": "id",
                "foreignField": "id_catalog",
                "as": "result"
            }
        },
        {
            "$group": {
                "_id": {
                    "id": "$id",
                    "name": "$name",
                    "plataform": "$plataform",
                    "description" : "$description",
                    "release_date": "$release_date",
                    "active": "$active",
                    "cost" : "$cost",
                    "discount" : "$discount"
                },
                "number_of_products": {
                    "$sum": { "$size": "$result" }
                }
            }
        },
        {
            "$project": {
                "_id": 0,
                "id": "$_id.id",
                "name": "$_id.name",
                "plataform": "$_id.plataform",
                "description" : "$_id.description",
                "release_date": "$_id.release_date",
                "active": "$_id.active",
                "cost" : "$_id.cost",
                "discount" : "$_id.discount",
                "number_of_products": 1
            }
        }
    ]


def get_catalog_sales_pipeline() -> list:
    return [
        {"$addFields": {
            "id_catalog_obj": {"$toObjectId": "$id_catalog"}
        }},
        {"$group": {
            "_id": "$id_catalog_obj",  
            "total_initial": {"$sum": "$initial_quantity"},
            "total_sold": {"$sum": "$sold_quantity"},
            "average_initial": {"$avg": "$initial_quantity"}
        }},
        {"$addFields": {
            "percent_sold": {"$cond": [{ "$eq": ["$total_initial", 0] }, 0 , { "$multiply": [{ "$divide": ["$total_sold", "$total_initial"] }, 100] }]},
            "id_catalog": {"$toString": "$_id"}
        }},
        {"$lookup": {
            "from": "catalogs",
            "localField": "_id",  
            "foreignField": "_id",
            "as": "catalog_info"
        }},
        {"$unwind": "$catalog_info"},
        {"$project": {
            "_id": 0,
            "id_catalog": "$id_catalog",
            "name": "$catalog_info.name",
            "total_units": "$total_initial",
            "average_units_per_lot": "$average_initial",
            "percent_sold": 1,
            "sold_units" : "$total_sold"
            }
        }
    ]



def get_discount_catalogs_pipeline() -> list:
   return [
        {"$match": {
           "active": True,
            "discount": { "$gt": 0 }
        }},
        {"$addFields": {
            "final_price": {"$round": [{"$subtract": ["$cost",{ "$multiply": [ "$cost", { "$divide": ["$discount", 100] } ] }]}, 2]}
        }},
        {"$project": {
            "_id": 0,
            "id": { "$toString": "$_id" },
            "name": 1,
            "plataform": 1,
            "original_price": "$cost",
            "discount_percent": "$discount",
            "final_price": "$final_price"
        }}
    ]

def validate_catalog_is_assigned_pipeline() -> list:
    return [
        {
            "$match": {
                "_id": ObjectId(id),
            }
        },
        {
            "$addFields": {
                "id": {"$toString": "$_id"}
            }
        },{
            "$lookup": {
                "from": "inventary",
                "localField": "id",
                "foreignField": "id_catalog",
                "as": "result"
            }
        },{
            "$group": {
                "_id": {
                    "id": "$id",
                    "name": "$name",
                    "active": "$active"
                },
                "number_of_products": {
                    "$sum": {"$size": "$result"}
                }
            }
        },{
            "$project": {
                "_id": 0,
                "id": "$_id.id",
                "name": "$_id.name",
                "active": "$_id.active",
                "number_of_products": 1
            }
        }
    ]