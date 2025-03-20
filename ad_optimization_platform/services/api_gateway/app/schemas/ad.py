from pydantic import BaseModel
from datetime import date
from enum import Enum, auto

class AdPlatform(str, Enum):
    google_ads = auto()
    meta_ads = auto()
    linkedin_ads = auto()

class AdFetchRequest(BaseModel):
    platform: AdPlatform
    start_date: date
    end_date: date

class AdFetchResponse(BaseModel):
    status: str
    batch_id: str