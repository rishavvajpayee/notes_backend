"""
Domain expansions for onBoarding the User
"""
from utils.authentication import encode_token, decode_token
from flask_sqlalchemy_session import current_session as session
from flask import g, request
from constants import common
from api.db.onboarding_db import User
import uuid
from sqlalchemy import or_



def signup():
    """
    checks if user exists | if not exists creates a new user
    can be modified to have a SMTP email verification added
    with a verify email / OTP added as a verification method
    """
    data = request.json
    try:
        user = session.query(User).filter(
            User.email == data["email"]
        ).first()
        if user:
            return 200, "user already exists", user.to_dict()
        new_user_id = uuid.uuid4()
        try:
            new_user = User(
                id = new_user_id,
                user_id = new_user_id,
                email = data["email"],
                phone_number = data["phone_number"],
            )
            new_user.save()
            accesstoken = encode_token(str(new_user_id))

            return 200, "user created find you token below", {
                "accesstoken" : accesstoken,
            }

        except Exception as error:
            return 400, f"Failed to create user : {error}", {}

    except Exception as e:
        return 500, f"BAD_REQUEST : {e}", {}


def login():
    """
    Checks if the user exists or not if yes Logs you in 
    else redirects the user to Sign up Page
    """
    data = request.json
    try:
        user: User = session.query(User).filter(
            or_(
                User.email == data["email"],
                User.phone_number == data["phone_number"]
            )
        )
        if user:
            user_obj = {}
            user_obj["user_id"] = user.user_id
            user_obj["email"] = user.email
            user_obj["phone_number"] = user.phone_number
            return 200, "logged in Successfully", user_obj

        return 400, "User not found please sign up", {}
        
    except Exception as e:
        return 400, "login failed", str(e)
