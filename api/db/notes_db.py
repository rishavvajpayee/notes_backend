from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from conf.base import Base


class Test(Base):
    __tablename__ = "Test"
    id = Column(Integer, primary_key=True)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    """Foreign key relationship with User"""
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", backref="notes")


class SharedNote(Base):
    """
    Shared Notes Db : holds note_id, shared with and shared_by details
    """

    __tablename__ = "shared_notes"

    id = Column(Integer, primary_key=True)
    note_id = Column(
        Integer, ForeignKey("notes.id", ondelete="CASCADE"), nullable=False
    )
    shared_with_user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    shared_by_user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    shared_at = Column(DateTime(timezone=True), server_default=func.now())

    """Relationships"""
    note = relationship("Note", backref="shared_notes")
    shared_with_user = relationship("User", foreign_keys=[shared_with_user_id])
    shared_by_user = relationship("User", foreign_keys=[shared_by_user_id])
