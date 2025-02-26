from datetime import datetime
from .base_model import BaseModel
from .user import User
from .place import Place

class Review(BaseModel):
    def __init__(self, text, rating, place: Place, user: User):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
