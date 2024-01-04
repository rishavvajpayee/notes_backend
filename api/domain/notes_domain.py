"""
Domain expansions for onBoarding Notes
"""

import random
from flask_sqlalchemy_session import current_session as session
from flask import g, request
from constants import common
from api.db.notes_db import Note


def get_notes():
    notes = session.query(Note).all()
    response = []
    if notes:
        for note in notes:
            note_object = {}
            note_object["id"] = note.id
            note_object["title"] = note.title
            note_object["content"] = note.content
            note_object["user_id"] = note.user_id
            response.append(note_object)

        return 200, common["SUCCESS"], response
    return 400, common["FAILURE"], {}

def post_notes():
    user_id = g.user_id
    

