from datetime import datetime
from .base_model import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner: User):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
