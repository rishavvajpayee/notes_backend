import jwt
from dotenv import load_dotenv
from conf.base import Config
from flask import g, request
from utils.responses import response_failure

load_dotenv()

SECRET_KEY = Config.SECRET_KEY


def encode_token(user_id):
    payload = {"user_id": user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return 200, payload
    except jwt.ExpiredSignatureError:
        return 400, {"user_id": None}
    except jwt.InvalidTokenError:
        return 400, {"user_id": None}


def is_authenticated(token):
    """
    decodes the token and checks if it exists in out DB
    """
    code, payload = decode_token(token)  # assume the user is authenticated at all times
    if code == 200:
        user_id = payload.get("user_id", None)
        return True, user_id
    else:
        return False, None


def before_check():
    url = request.path
    whitelist_api = (
        Config.WHITELIST_API.replace(" ", "").split(",") if Config.WHITELIST_API else []
    )
    if request.method == "OPTIONS" or url in whitelist_api:
        return None

    if "Accesstoken" in request.headers:
        token = request.headers["Accesstoken"]
        authenticated, valid_user_token = is_authenticated(token)

        if authenticated:
            g.user_id = valid_user_token
            return None
        return response_failure(400, "Token Validation failed", {})
    return response_failure(400, "Invalid Request | accesstoken not provided", {})
