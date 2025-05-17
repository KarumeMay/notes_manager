from extensions import db
from models.note import Note


def get_notes_for_user(user_id, search=None, tag=None):
    q = Note.query.filter_by(user_id=user_id)
    if search:
        q = q.filter(Note.title.contains(search))
    if tag:
        q = q.join('category').filter_by(name=tag)
    return q.all()
