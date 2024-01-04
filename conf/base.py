import enum
from .api_error import ServerError
from conf.database import Config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import text, inspect, DateTime, String, Boolean, Column, Enum
from flask_sqlalchemy_session import current_session as session
from flask import g

Session = sessionmaker(bind=Config.engine, autoflush=False)
base = declarative_base()


class EnumStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPEND = "SUSPEND"


class Base(base):
    __abstract__ = True
    status = Column(Enum(EnumStatus), server_default="ACTIVE")
    created_on = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        server_default=text("NOW()"),
    )
    updated_on = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=text("NOW()"),
    )
    deleted_on = Column(DateTime(timezone=True), server_default=None)
    created_by = Column(String(50), server_default="")
    deleted_by = Column(String(50), server_default="")
    updated_by = Column(String(50), server_default="")
    is_deleted = Column(Boolean, default=False, server_default=text("FALSE"))

    def serialize(self):
        """return a json-serializable version of the object"""
        return {c: getattr(self, c) for c in self.__serialize_attributes__}

    def to_dict(self):
        """return all attributes as json object"""
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    def save(self):
        user_id = getattr(g, "user_id", "")
        self.created_by = user_id
        session.add(self)
        commit()

    def delete(self):
        user_id = getattr(g, "user_id", "")
        self.deleted_by = user_id
        self.is_deleted = True
        session.delete(self)
        commit()

    def soft_delete(self):
        user_id = getattr(g, "user_id", "")
        self.status = "INACTIVE"
        self.deleted_by = user_id
        self.deleted_on = datetime.now()
        self.is_deleted = True
        commit()

    def update(self, attributes=None):
        """update object with attributes list"""
        user_id = getattr(g, "user_id", "")
        self.updated_by = user_id
        commit()

    def update_with_list(self):
        for val in self:
            val.update()

    def save_without_commit(self):
        user_id = getattr(g, "user_id", "")
        self.created_by = user_id
        session.add(self)
        flush()

    def update_without_commit(self, attributes):
        user_id = getattr(g, "user_id", "")
        self.updated_by = user_id
        for key, value in attributes.items():
            setattr(self, key, value)
        flush()

    def delete_without_commit(self):
        user_id = getattr(g, "user_id", "")
        self.deleted_by = user_id
        self.is_deleted = True
        session.delete(self)
        flush()


def query(session, cls):
    return session.query(cls).filter_by(is_deleted=False)


def commit():
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise ServerError(str(e))


def flush():
    try:
        session.flush()
    except Exception as e:
        session.rollback()
        raise ServerError(str(e))
