from constants import common
from flask import Blueprint, request
from utils.responses import Responses, response_success, response_failure, handle_response

"""
IMPORT DOMAIN FUNCTIONS :
"""
from api.domain.onboarding_domain import login, otp_verify, signup

AUTHENTICATION_BLUEPRINT = Blueprint("login", __name__, url_prefix="/api/auth/")


@AUTHENTICATION_BLUEPRINT.route("signup", methods=["POST"])
def post_signup():
    code, message, result = signup()
    handle_response(code, message, result)


@AUTHENTICATION_BLUEPRINT.route("login", methods=["POST"])
def post_login():
    code, message, result = login()
    handle_response(code, message, result)


@AUTHENTICATION_BLUEPRINT.route("otp_verify", methods=["POST"])
def otp_verification():
    code, message, result = otp_verify()
    handle_response(code, message, result)
