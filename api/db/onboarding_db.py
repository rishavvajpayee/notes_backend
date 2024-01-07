from conf.base import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), default=func.uuid_generate_v4(), primary_key=True)
    user_id = Column(UUID(as_uuid=True), default=func.uuid_generate_v4())
    email = Column(String(100), default=None)
    phone_number = Column(String(100), default=None)
    password = Column(String(100), default=None)
