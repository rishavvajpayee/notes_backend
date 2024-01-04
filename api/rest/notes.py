"""
1. GET /api/notes: get a list of all notes for the authenticated user.
3. POST /api/notes: create a new note for the authenticated user.


2. GET /api/notes/:id: get a note by ID for the authenticated user.
4. PUT /api/notes/:id: update an existing note by ID for the authenticated user.
5. DELETE /api/notes/:id: delete a note by ID for the authenticated user.


6. POST /api/notes/:id/share: share a note with another user for the authenticated user.
7. GET /api/search?q=:query: search for notes based on keywords for the authenticated user.
"""

from constants import common
from flask import Blueprint, request
from utils.responses import handle_response

"""
Import Domain Functions : 
"""
from api.domain.notes_domain import get_notes, post_notes


NOTES_BLUEPRINT = Blueprint("notes", __name__, url_prefix="/api/")


@NOTES_BLUEPRINT.route("notes", methods=["GET","POST"])
def post_signup():
    if request.method == "GET":
        code, message, result = get_notes()
    elif request.method == "POST":
        code, message, result = post_notes()
    handle_response(code, message, result)
