from datetime import datetime
from .base_model import BaseModel
<<<<<<< HEAD
from app.persistence.repository import inMemoryRepository as database
from flask_bcrypt import bcrypt
bcrypt = Bcrypt()
import uuid
=======
>>>>>>> 5b2692a01f2ba9ee7c54a7447ed8a7fa46021032

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.hash_password(password)
        self.is_admin = is_admin
        self.validate_user()

    def hash_password(self, password):
        from app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        from app import bcrypt
        return bcrypt.check_password_hash(self.password, password)

    def validate_user(self):
        if not self.first_name
            raise ValueError("First name is required")
        if not self.last_name
            raise ValueError("Last name is required")
        if not self.email
            raise ValueError("Email is required")
        emailregex = r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+.[a-zA-Z]{2,}$'
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")
        if not self.password
            raise ValueError("Password is required")

class Admin(User):
    def __promote(self, user_id):
        if self.is_admin == True:
            update_date = datetime.now()
            if database.update(self, user_id, {"is_admin": True, "update_date": update_date}) is not None:
                print("User promotion to Admin")
                return True
            return False

    def __demote(self, user_id):
        if self.is_admin == False:
            update_date = datetime.now()
            if database.update(self,user_id, {"is_admin": True, "update_date": update}) is not None:
                print("User is no longer Admin")
                return True
            return False
