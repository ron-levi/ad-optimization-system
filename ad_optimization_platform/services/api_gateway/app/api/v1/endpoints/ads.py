from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ad import AdFetchRequest, AdFetchResponse
from app.services.ad_service import fetch_ad_data

router = APIRouter()

@router.post("/fetch", response_model=AdFetchResponse)
async def trigger_ad_data_fetch(request: AdFetchRequest):
    result = await fetch_ad_data(platform=request.platform, start_date=request.start_date, end_date=request.end_date)
    if not result.success:
        raise HTTPException(status_code=500, detail="Data fetch failed.")
    return AdFetchResponse(status="fetch_started", batch_id=result.batch_id)