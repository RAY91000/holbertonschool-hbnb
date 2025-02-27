from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ----- User Methods -----
    def create_user(self, user_data):
        if not user_data.get("email") or not user_data.get("password"):
            raise ValueError("Email and password are required")
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)
    
    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        return self.user_repo.get_all()
    
    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        for key, value in user_data.items():
            setattr(user, key, value)
        self.user_repo.update(user)
        return user

    def delete_user(self, user_id):
        return self.user_repo.delete(user_id)

    # ----- Place Methods -----
    def create_place(self, place_data):
        if "title" not in place_data or "price" not in place_data:
            raise ValueError("Title and price are required")
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        for key, value in place_data.items():
            setattr(place, key, value)
        self.place_repo.update(place)
        return place

    def delete_place(self, place_id):
        return self.place_repo.delete(place_id)
    
    # ----- Amenity Methods -----
    def create_amenity(self, amenity_data):
        if "name" not in amenity_data:
            raise ValueError("Amenity name is required")
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        self.amenity_repo.update(amenity)
        return amenity
    
    def delete_amenity(self, amenity_id):
        return self.amenity_repo.delete(amenity_id)
    
    # ----- Review Methods -----
    def create_review(self, review_data):
        if "rating" not in review_data or "user_id" not in review_data or "place_id" not in review_data:
            raise ValueError("Rating, user_id, and place_id are required")
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]
    
    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        for key, value in review_data.items():
            setattr(review, key, value)
        self.review_repo.update(review)
        return review
    
    def delete_review(self, review_id):
        return self.review_repo.delete(review_id)
    