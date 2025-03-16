from fastapi import APIRouter
from .endpoints import auth, ads, analytics, optimization, ai, health

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(ads.router, prefix="/ads", tags=["Ads"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(optimization.router, prefix="/optimization", tags=["Optimization"])
api_router.include_router(ai.router, prefix="/ai", tags=["AI"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])