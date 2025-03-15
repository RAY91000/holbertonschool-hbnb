import re
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from .base_model import BaseModel, Base

bcrypt = Bcrypt()

class User(BaseModel, Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.set_password(password)
        self.validate_user()

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def validate_user(self):
        if not self.first_name:
            raise ValueError("First name is required")
        if not self.last_name:
            raise ValueError("Last name is required")
        if not self.email:
            raise ValueError("Email is required")
        email_regex = r"^[a-zA-Z0-9.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, self.email):
            raise ValueError("Invalid email format")
        if not self.password:
            raise ValueError("Password is required")

class Admin(User):
    def promote(self, user):
        if self.is_admin:
            user.is_admin = True
            user.updated_at = datetime.utcnow()
            return True
        return False

    def demote(self, user):
        if self.is_admin and user.is_admin:
            user.is_admin = False
            user.updated_at = datetime.utcnow()
            return True
        return False

