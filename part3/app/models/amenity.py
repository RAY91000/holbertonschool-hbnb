from sqlalchemy import Column, String, DateTime
from datetime import datetime
import uuid
from .base_model import BaseModel, Base

class Amenity(BaseModel, Base):
    __tablename__ = "amenities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name):
        super().__init__()
        self.name = name

