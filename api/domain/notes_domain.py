"""
Domain expansions for Notes
"""

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
    return 200, "notes not found", {}

def post_notes():
    user_id = g.user_id
    data = request.json

    try:
        note = session.query(Note).filter(
            Note.user_id == user_id,
            Note.title == data["title"]
        ).all()

        if note:
            response = {}
            response["id"] = note.id
            response["title"] = note.title
            response["content"] =  note.content
            response["user_id"] = note.user_id

            return 200, "Note already Exist", response 
        else:
            try :
                new_note = Note(
                    user_id = g.user_id,
                    title = data["title"],
                    content = data["content"]
                )
                new_note.save()
                return 200, "note creation successfull", new_note.to_dict()
        
            except Exception as error:
                return 400, f"failed : {error}", {}
    except Exception as error:
        return 500, f"Failed : {error}", {}
