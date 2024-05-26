#!/usr/bin/env python3
""" """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Post(BaseModel, Base):
    """Representation of a post"""
    __tablename__ = "posts"

    user_id = Column(String(60), ForeignKey(
        'users.id', ondelete='CASCADE'), nullable=False)
    content = Column(String(1024))
    media_type = Column(String(60))
    media_url = Column(String(255))

    user = relationship('User', back_populates='posts')

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the post instance"""
        super().__init__(*args, **kwargs)
