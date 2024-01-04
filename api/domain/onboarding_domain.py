"""
Domain expansions for onBoarding the User
"""

from flask_sqlalchemy_session import current_session as session
from flask import g, request
from constants import common
from api.db.onboarding_db import User
import uuid


def signup():
    try:
        user = session.query(User).filter(
            User.user_id == g.user_id
        ).first()
        if user:
            return 200, "user already exists", user.to_dict()
    except Exception as e:
        return 400, "BAD_REQUEST", str(e)


def login():
    try:
        ...
    except Exception as e:
        return 400, "LOGIN FAILED", str(e)
