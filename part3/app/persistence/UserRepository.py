from sqlalchemy.orm import Session
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: User):
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_by_id(self, user_id: str):
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str):
        return self.db_session.query(User).filter(User.email == email).first()

    def update(self, user_id: str, updated_data: dict):
        user = self.get_by_id(user_id)
        if user:
            for key, value in updated_data.items():
                setattr(user, key, value)
            self.db_session.commit()
            self.db_session.refresh(user)
            return user
        return None

    def delete(self, user_id: str):
        user = self.get_by_id(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
            return True
        return False

    def get_user_places(self, user_id: str):
        return self.db_session.query(Place).filter(Place.owner_id == user_id).all()

    def get_user_reviews(self, user_id: str):
        return self.db_session.query(Review).filter(Review.user_id == user_id).all()

    def get_user_amenities(self, user_id: str):
        return self.db_session.query(Amenity).join(
            Place.amenities
        ).filter(Place.owner_id == user_id).all()

