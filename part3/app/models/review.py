from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from .base_model import BaseModel, Base

class Review(BaseModel, Base):
    __tablename__ = "reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(36), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict_with_ids(self):
        review_dict = self.to_dict()
        review_dict['place_id'] = self.place_id
        review_dict.pop('place', None)
        review_dict['user_id'] = self.user_id
        review_dict.pop('user', None)
        return review_dict

