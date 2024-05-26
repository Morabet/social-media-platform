#!/usr/bin/env python3
"""
Contains class BaseModel
"""

from models.base_model import Base, BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import bcrypt


class User(BaseModel, Base):
    """Representation of a user"""
    __tablename__ = "users"

    user_name = Column(String(128), unique=True)
    name = Column(String(128))
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    bio = Column(String(128))
    profile_picture_url = Column(String(128))

    posts = relationship('Post', back_populates='user',
                         cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """Initializing the user instance"""
        if 'password' in kwargs and isinstance(kwargs['password'], str):
            kwargs['password'] = self.password_hashing(kwargs['password'])
        super().__init__(*args, **kwargs)

    def password_hashing(self, pwd: str):
        """Hash the password using bcrypt"""
        hashed = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    def verify_password(self, pwd: str) -> bool:
        """Verify the password"""
        return bcrypt.checkpw(pwd.encode('utf-8'), self.password.encode('utf-8'))
