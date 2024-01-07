from utils.responses import handle_response
from flask import Blueprint

"""
IMPORT DOMAIN FUNCTIONS :
"""
from api.domain.onboarding_domain import login, signup

AUTHENTICATION_BLUEPRINT = Blueprint("login", __name__, url_prefix="/api/auth/")


@AUTHENTICATION_BLUEPRINT.route("signup", methods=["POST"])
def post_signup():
    code, message, result = signup()
    return handle_response(code, message, result)


@AUTHENTICATION_BLUEPRINT.route("login", methods=["POST"])
def post_login():
    code, message, result = login()
    return handle_response(code, message, result)
