from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from bson import ObjectId
from database import db  # adjust this path if needed

router = APIRouter()

@router.get("/services")
async def get_services(
    search: Optional[str] = "",
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "name",
    sort_order: int = 1  # 1 = asc, -1 = desc
):
    query = {"is_active": True}
    
    if search:
        query["name"] = {"$regex": search, "$options": "i"}
    if category:
        query["category"] = category

    services_cursor = db.services.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
    services = await services_cursor.to_list(length=limit)

    for s in services:
        s["_id"] = str(s["_id"])  # Convert ObjectId to string for frontend

    total = await db.services.count_documents(query)

    return {"data": services, "total": total}

# -----------------------------------------------
# ✅ NEW ROUTE - GET SINGLE SERVICE BY ID
# -----------------------------------------------
@router.get("/services/{service_id}")
async def get_service_by_id(service_id: str):
    try:
        service = await db.services.find_one({"_id": ObjectId(service_id)})
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid service ID format")

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    service["_id"] = str(service["_id"])  # Convert ObjectId to string
    return service
