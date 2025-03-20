from sqlalchemy import Column, String, Date, Enum
from app.db.base import Base

class AdCampaign(Base):
    __tablename__ = "ad_campaigns"

    id = Column(String, primary_key=True, index=True)
    platform = Column(Enum("google_ads", "meta_ads", "linkedin_ads"), nullable=False)
    campaign_name = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)